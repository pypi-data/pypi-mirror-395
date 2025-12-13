import os
import time
from redis import StrictRedis

REDIS_DB = os.environ['REDIS_DB']
REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PREFIX = os.environ.get('REDIS_PREFIX', '')


class RateLimit(StrictRedis):
    def __init__(self):
        super().__init__(host=REDIS_SERVER, db=REDIS_DB)

    def current_milli_time(self):
        return int(round(time.time() * 1000))

    def is_blocked(self, identifier, action):
        """Verifica se o identificador está bloqueado."""
        block_key = f"{REDIS_PREFIX}:block:{action}:{identifier}"
        return self.exists(block_key) > 0

    def track_failure(self, identifier, action="login", max_attempts=5, block_duration=900000):
        """Rastreia falhas e aplica bloqueio após exceder o limite."""
        failure_key = f"{REDIS_PREFIX}:failures:{action}:{identifier}"
        p = self.pipeline()
        p.incr(failure_key)
        p.expire(failure_key, block_duration // 1000)
        count, _ = p.execute()
        if count >= max_attempts:
            block_key = f"{REDIS_PREFIX}:block:{action}:{identifier}"
            self.setex(block_key, block_duration // 1000, "blocked")
            return {"blocked": True, "reason": "Too many failed attempts"}
        return {"blocked": False}

    def track_pattern(self, identifier, action="abuse"):
        """Detecta padrões de requisições regulares (baixa frequência)."""
        pattern_key = f"{REDIS_PREFIX}:rate_limit:pattern:{action}:{identifier}"
        now = self.current_milli_time()
        last_req = self.get(f"{pattern_key}:last")
        last_req = int(last_req) if last_req else now
        interval = now - last_req
        self.set(f"{pattern_key}:last", now)

        p = self.pipeline()
        p.lpush(f"{pattern_key}:intervals", interval)
        p.ltrim(f"{pattern_key}:intervals", 0, 9)
        p.expire(f"{pattern_key}:intervals", 3600)
        p.execute()

        intervals = self.lrange(f"{pattern_key}:intervals", 0, -1)
        if len(intervals) > 5:
            intervals = [int(i) for i in intervals]
            mean = sum(intervals) / len(intervals)
            variance = sum((x - mean) ** 2 for x in intervals) / len(intervals)
            if variance < 100:
                block_key = f"{REDIS_PREFIX}:block:{action}:{identifier}"
                self.setex(block_key, 300, "suspicious")
                return {"suspicious": True, "reason": "Regular request intervals"}
        return {"suspicious": False}

    def check_limits(self, identifier, limits, limit_type=None):
        """Verifica limites de taxa e abuso."""
        if identifier == '127.0.0.1':
            return {
                "rate_limited": False,
                "abuse": False,
                "blocked": False
            }

        action = limit_type if limit_type else "api"
        if self.is_blocked(identifier, action):
            return {"rate_limited": True, "abuse": False, "blocked": True}

        if action in ["api", "login"]:
            pattern_result = self.track_pattern(identifier, "abuse")
            if pattern_result["suspicious"]:
                return {"rate_limited": True, "abuse": True, "reason": pattern_result["reason"]}

        now = self.current_milli_time()
        type_to_check = action
        key_prefix = f"{REDIS_PREFIX}:rate_limit:{type_to_check}"

        # Obtém configuração do limite específico
        limit_configs = limits.get(type_to_check, limits["api"])
        if not isinstance(limit_configs, list):
            limit_configs = [limit_configs]
        limit_abuse_configs = limits["abuse"]

        p = self.pipeline()

        # Operações para o tipo específico (api ou login)
        for config in limit_configs:
            key = f"{key_prefix}:{config['interval']}:{identifier}"
            p.zremrangebyscore(key, 0, now - config["interval"])
            p.zcard(key)
            p.zadd(key, {f"req_{now}": now})
            p.expire(key, int(config["interval"] / 1000) + 1)

        # Operações para abuso
        abuse_results = []
        for config in limit_abuse_configs:
            abuse_key = f"{REDIS_PREFIX}:rate_limit:abuse:{config['interval']}:{identifier}"
            p.zremrangebyscore(abuse_key, 0, now - config["interval"])
            p.zcard(abuse_key)
            p.zadd(abuse_key, {f"req_{now}": now})
            p.expire(abuse_key, int(config["interval"] / 1000) + 1)
            abuse_results.append(config["limit"])

        pipeline_results = p.execute()

        # Resultados para o tipo específico
        is_rate_limited = False
        for i, config in enumerate(limit_configs):
            count_type = pipeline_results[i * 4 + 1]
            if count_type >= config["limit"]:
                is_rate_limited = True

        # Resultados para abuso
        is_abuse = False
        for i, config_limit in enumerate(abuse_results):
            count_abuse = pipeline_results[(len(limit_configs) * 4) + (i * 4) + 1]
            if count_abuse >= config_limit:
                is_abuse = True

        return {
            "rate_limited": is_rate_limited,
            "abuse": is_abuse,
            "blocked": False
        }

    def api_limited(self, identifier, limits):
        """Verifica limite para requisições de API."""
        return self.check_limits(identifier, limits, "api")

    def login_limited(self, identifier, limits):
        """Verifica limite para tentativas de login."""
        return self.check_limits(identifier, limits, "login")


RateLimiter = RateLimit()
