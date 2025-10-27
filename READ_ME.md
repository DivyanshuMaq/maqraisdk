# RAI Agent

Lightweight framework for orchestration of AI agents (reviewer, updater, testcase generator) built on top of crewai and OpenAI-compatible LLM backends.

## Features

- Review and improve input prompts using configurable review/update agents
- Generate policy-compliant test cases
- Pluggable LLM connections (OpenAI-compatible clients or custom LLMs)
- YAML-driven agent and task configuration
- Logging and telemetry integration (Application Insights / crewai listener)

## Quick start

1. Clone the repository and create a virtual environment (recommended).
2. Install dependencies:

   pip install -r requirements.txt

3. Create a `.env` file in the package root with your OpenAI / LLM settings. Required keys used by `main.py`:

   ```env
   OpenAI_Key=your_api_key_here
   OpenAI_endpoint=https://api.openai.com
   OpenAI_deployment=your_deployment_name
   ```

4. Configure agents and tasks using the YAML files in `config/` (examples provided in the repo).

5. Run the example script to see the agents in action:

   python main.py

   Note: `main.py` is an interactive demo and will prompt for the number of test cases and categories when generating test cases.

6. Optionally run `startup.py` to initialize crewai console integration and Application Insights logging.

## Project layout

- `main.py` — Example entrypoint demonstrating reviewer, updater and testcase generator utilities.
- `startup.py` — Initializes crewai console wrapper that forwards console output into the crewai logger (and Application Insights listener).
- `agents/` — Implementations of high-level agents (reviewer, testcase generator, updater).
- `crew/` — Crew (orchestration) related helpers used by the system.
- `config/` — YAML configuration for agents and tasks (editable to customize behavior and pipelines).
- `connections/` — LLM client implementations (OpenAI client, custom LLM adapter).
- `tasks/` — Task wrappers that agents use to perform work.
- `utility/` — Prompt utilities and shared helpers for reviewer/updater/testcase generation logic.
- `Success_metrics/` — Helpers for calculating and reporting task success metrics.
- `Application_insights.py` and `crewai_logger_listener.py` — Telemetry & logging integration code.

## Folder details

Below are concise explanations for the most important folders in this repository and how they interact.

### agents/
- Purpose: Instantiate and configure crewai Agent objects for specific responsibilities (review, update, test-case generation).
- Key modules:
  - `reviewer_agents.py` — `reviewerAgents` loads `config/reviewer_agents.yaml`, requires a `CustomLLM` and returns reviewer Agent instances (senior, XPIA, groundedness, jailbreak, harmful content).
  - `testcase_generator_agents.py` — `testcaseGeneratorAgents` produces generator Agents used to create adversarial or compliance-focused test cases.
  - `updater_agents.py` — `updaterAgents` exposes agents that apply feedback and produce updated prompts.
- Notes: Agents are created with `llm` instances produced by `CustomLLM` and expose `get_*_agents()` methods that return dicts of crewai Agent objects.

### config/
- Purpose: Central place for YAML-driven configuration that controls agent behavior, task parameters, templates, and limits.
- Files of interest:
  - `reviewer_agents.yaml` / `reviewer_tasks.yaml`
  - `testcase_generator_agents.yaml` / `testcase_generator_tasks.yaml`
  - `updater_agents.yaml` / `updater_tasks.yaml`
- Notes: YAML files may include simple templating (e.g. `{{num_cases}}`) which the code replaces before parsing. Edit these files to change prompts, agent settings, `max_tokens`, or task-level options.

### connections/
- Purpose: Encapsulate LLM provider integration and adapt provider-specific clients into the crewai `LLM` interface.
- Key modules:
  - `open_ai.py` — `OpenAIClient` wraps endpoint/key/deployment settings and exposes configuration used to build an LLM client.
  - `custom_llm.py` — `CustomLLM` builds a `crewai.LLM` from an `OpenAIClient` (sets model, temperature, top_p, base_url, api_key).
- Notes: Instantiate `OpenAIClient` with `.env` values (see Quick start) and pass it to `CustomLLM` before creating agents or crews.

### crew/
- Purpose: Assemble related agents and tasks into higher-level `Crew` objects that run the orchestration for a capability.
- Key modules:
  - `reviewer_crew.py` — `reviewerCrew` constructs a `Crew` containing reviewer agents and tasks (sequential process, caching, RPM limits).
  - `testcase_generator_crew.py` — builds a crew for generating test cases from prompts.
  - `updater_crew.py` — builds a crew that applies reviewer feedback to produce updated prompts.
- Notes: Crews centralize lifecycle options (process model, caching, rate limits) and are the primary runtime objects kicked off by utility classes.

### Success_metrics/
- Purpose: Provide utilities to measure and report how well generated content and agents perform against RAI criteria.
- Key modules:
  - `Task_success_rate.py` — runs generated test cases through the model, evaluates compliance per category (HarmfulContent, Jailbreak, XPIA, Groundedness) and computes per-category and overall success metrics.
  - `compliance.py` — helper utilities related to compliance checks (see file for details).
- Notes: These modules call LLM APIs to evaluate model outputs and return numeric metrics and detailed result lists.

### tasks/
- Purpose: Create crewai `Task` objects that bind an agent to a configuration block from YAML and control execution semantics.
- Key modules:
  - `reviewer_tasks.py` — `reviewerTasks` loads reviewer task definitions and maps them to reviewer agents.
  - `testcase_generator_tasks.py` — `testcaseGeneratorTasks` supports `num_cases` substitution and category filtering for generator tasks.
  - `updater_tasks.py` — `updaterTasks` maps updater agents to their task definitions.
- Notes: Tasks are the execution units a `Crew` runs; they accept agent objects and task configs and return outputs that utilities parse as JSON.

### utility/
- Purpose: Small, user-facing helper classes that provide straightforward APIs used by `main.py` and other callers.
- Key modules:
  - `promptReviewer.py` — `PromptReviewer` uses `reviewerCrew` to run a prompt through the reviewer pipeline and returns the senior review output as a dict. It includes retry logic for transient policy-validation failures.
  - `promptUpdater.py` — `PromptUpdater` applies reviewer feedback to update prompts via the updater crew.
  - `promptTestcaseGenerator.py` — `promptTestcaseGenerator` invokes the generator crew to create RAI-focused test cases (supports `num_cases` and category filters).
- Notes: These wrapper classes are the most convenient entry points when embedding the library in other tooling or demos.

## Configuration

- Agent and task behavior is configured with YAML files located in `config/` (e.g. `reviewer_agents.yaml`, `testcase_generator_tasks.yaml`). Edit those files to change prompts, categories, thresholds, or agent routing.
- Environment variables (via `.env`) are used to provide secrets and endpoints for external services (see Quick start).

Example minimal agent YAML (illustrative only):

```yaml
agents:
  - name: reviewer
    model: gpt-4
    max_tokens: 1024
    temperature: 0.1
```

## Extending

- To add a new agent type: add a Python module in `agents/`, add configuration in `config/`, and register/instantiate the agent where needed (e.g. in `main.py` or a new orchestration script).
- To support another LLM provider: implement a new client under `connections/` that follows the same interface used by `OpenAIClient` and `CustomLLM`.

## Logging & Telemetry

- `crewai_logger_listener.py` contains a listener (`MyCustomListener`) used to forward crewai logs to Application Insights or any other telemetry pipeline.
- `startup.py` shows an example of wrapping the crewai console so console output is captured by the logger.

## Troubleshooting

- If the application fails to contact the LLM, verify `.env` values (`OpenAI_Key`, `OpenAI_endpoint`, `OpenAI_deployment`).
- If native dependencies fail (e.g. `onnxruntime`), ensure the environment matches the package requirements and the correct wheels are installed for your OS/Python.

## Development

- Tests are not included by default. Add a `tests/` directory and use `pytest` or preferred test framework.
- Follow standard Python packaging and linting practices. Consider adding a `pyproject.toml` and `tox`/`nox` for CI workflows.

## Contributing

- Open an issue or submit a pull request with a clear description of the change. Maintain backward compatibility for public interfaces where possible.

## License

- No license file is included in this repository. Add a `LICENSE` file if you intend to make this project public and define reuse terms.

## Contact

- For questions or support, open an issue in the repository with a minimal reproduction and relevant logs.
