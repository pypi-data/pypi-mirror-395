from fbnconfig import Deployment, identity


def configure(env):
    application = identity.ApplicationResource(
        id="test_app",
        client_id="robTest-app-client",
        display_name="robTest Application",
        type=identity.ApplicationType.NATIVE,
    )
    return Deployment("application", [application])
