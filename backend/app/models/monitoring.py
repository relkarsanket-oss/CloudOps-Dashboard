from pydantic import BaseModel


class MonitoringData(BaseModel):
    ec2: list[dict]
    s3: list[dict]
    rds: list[dict]


class MonitoringError(BaseModel):
    status: str
    message: str