Feature: GitHub Actions Workflow Validation with Ghanon

	Scenario: Without Arguments
		Given I have installed the CLI
		When I run without arguments
		Then I should see all the workflows under `.github/workflows` validated

	Scenario: Multiple Positional Arguments
		Given I have installed the CLI
		When I pass it two valid workflows
		Then I should see two workflows validated

	Scenario Outline: Valid Cases
		Given a workflow "<workflow>"
		When I parse it
		Then the validation should pass
		And I should see message "<workflow>" is a valid workflow

		Examples:
			| workflow             |
			| simple_workflow.yml  |
			| complex_workflow.yml |

	Scenario Outline: Error Cases
		Given a workflow "<workflow>"
		When I parse it
		Then the validation should fail
		And I should see message "<error>"

		Examples:
			| workflow                        | error                                                                                                                    |
			| nonexistent.yml                 | File 'nonexistent.yml' does not exist                                                                                    |
			| README.md                       | Input should be a valid dictionary or instance of Workflow                                                               |
			| pyproject.toml                  | Error parsing YAML                                                                                                       |
			| invalid_key.yml                 | Error parsing workflow file                                                                                              |
			| secrets_inherit.yml             | Do not use `secrets: inherit` with reusable workflows as it can be insecure                                              |
			| no_permissions.yml              | Jobs should specify `contents: read` permission at minimum to satisfy the principle of least privilege                   |
			| no_permissions_reusable_job.yml | Reusable workflow jobs should specify `contents: read` permission at minimum to satisfy the principle of least privilege |
			| no_content_permissions.yml      | When modifying the default permissions, `contents: read/write` is explicitly required                                    |
