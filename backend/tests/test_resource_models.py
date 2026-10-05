from backend.app.models.resources import (
    EC2Resource,
    RDSResource,
    S3Resource,
    ResourceError,
    ResourceResponse,
)


def test_ec2_resource_model():
    resource = EC2Resource(
        instance_id="i-1234567890abcdef0",
        instance_type="t3.micro",
        state="running",
        private_ip="10.0.1.10",
        public_ip="203.0.113.10",
    )

    assert resource.instance_id == "i-1234567890abcdef0"
    assert resource.instance_type == "t3.micro"
    assert resource.state == "running"


def test_rds_resource_model():
    resource = RDSResource(
        db_instance_identifier="cloudops-db",
        engine="postgres",
        status="available",
        instance_class="db.t3.micro",
        endpoint="cloudops-db.example.com",
    )

    assert resource.db_instance_identifier == "cloudops-db"
    assert resource.engine == "postgres"
    assert resource.status == "available"


def test_s3_resource_model():
    resource = S3Resource(
        name="securesync-iot-387512137867",
        creation_date="2026-08-20T12:04:00+00:00",
    )

    assert resource.name == "securesync-iot-387512137867"
    assert resource.creation_date is not None


def test_resource_response_model():
    resource = ResourceResponse(
        resources=[
            EC2Resource(
                instance_id="i-1234567890abcdef0",
                instance_type="t3.micro",
                state="running",
            )
        ]
    )

    assert len(resource.resources) == 1
    assert resource.resources[0].instance_id == "i-1234567890abcdef0"


def test_resource_error_model():
    error = ResourceError(
        status="error",
        message="Unable to retrieve EC2 resources",
    )

    assert error.status == "error"
    assert error.message == "Unable to retrieve EC2 resources"