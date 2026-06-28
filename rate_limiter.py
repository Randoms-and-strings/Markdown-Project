class RateLimiter:
    def __init__(self, bucket_size:int = 10, refill_rate:int = 1, refill_interval:int = 60):
        self.bucket = bucket_size
        self.refill_rate = refill_rate
        self.fill_interval = refill_interval

        # self.user_token = user_token
    def