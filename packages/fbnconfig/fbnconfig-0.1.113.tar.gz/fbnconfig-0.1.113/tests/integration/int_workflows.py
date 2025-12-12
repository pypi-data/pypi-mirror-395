import os
from types import SimpleNamespace

from pytest import fixture

import fbnconfig
from tests.integration import workflows
from tests.integration.generate_test_name import gen

if os.getenv("FBN_ACCESS_TOKEN") is None or os.getenv("LUSID_ENV") is None:
    raise (
        RuntimeError("Both FBN_ACCESS_TOKEN and LUSID_ENV variables need to be set to run these tests")
    )

lusid_env = os.environ["LUSID_ENV"]
token = os.environ["FBN_ACCESS_TOKEN"]
host_vars = {}
client = fbnconfig.create_client(lusid_env, token)


@fixture
def setup_deployment():
    deployment_name = gen("workflows")
    print(f"\nRunning for deployment {deployment_name}...")
    yield SimpleNamespace(name=deployment_name)
    # Teardown: Clean up resources (if any) after the test
    print("\nTearing down resources...")
    fbnconfig.deployex(fbnconfig.Deployment(deployment_name, []), lusid_env, token)


def test_teardown(setup_deployment):
    # create first
    fbnconfig.deployex(workflows.configure(setup_deployment), lusid_env, token)
    fbnconfig.deployex(fbnconfig.Deployment(setup_deployment.name, []), lusid_env, token)
    result = client.get(f"/workflow/api/workers?filter=id.scope eq '{setup_deployment.name}'")
    # no response returned
    assert len(result.json()["values"]) == 0


def test_create(setup_deployment):
    fbnconfig.deployex(workflows.configure(setup_deployment), lusid_env, token)
    workers = client.get(f"/workflow/api/workers?filter=id.scope eq '{setup_deployment.name}'")
    task_defs = client.get(f"/workflow/api/taskdefinitions?filter=id.scope eq '{setup_deployment.name}'")
    event_handlers = client.get(
        f"/workflow/api/eventhandlers?filter=id.scope eq '{setup_deployment.name}'"
    )
    assert len(workers.json()["values"]) == 1
    assert len(task_defs.json()["values"]) == 1
    assert len(event_handlers.json()["values"]) == 2


def test_update_nochange(setup_deployment):
    fbnconfig.deployex(workflows.configure(setup_deployment), lusid_env, token)
    actions = fbnconfig.deployex(workflows.configure(setup_deployment), lusid_env, token)
    assert {a.change for a in actions} == {"nochange", "attach"}
    workers = client.get(f"/workflow/api/workers?filter=id.scope eq '{setup_deployment.name}'")
    task_defs = client.get(f"/workflow/api/taskdefinitions?filter=id.scope eq '{setup_deployment.name}'")
    event_handlers = client.get(
        f"/workflow/api/eventhandlers?filter=id.scope eq '{setup_deployment.name}'"
    )
    assert len(workers.json()["values"]) == 1
    assert len(task_defs.json()["values"]) == 1
    assert len(event_handlers.json()["values"]) == 2
