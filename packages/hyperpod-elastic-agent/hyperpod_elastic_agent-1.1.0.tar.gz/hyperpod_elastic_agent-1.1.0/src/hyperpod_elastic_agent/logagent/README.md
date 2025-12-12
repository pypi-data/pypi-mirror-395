# Log Monitoring Agent

This module is the implementation of [this](https://quip-amazon.com/NbqIAMsI2Ifs/Hyperpod-Compass-data-plane-low-level-design) Log Agent design.

To enable the Log Agent, customers must specify the environment variable `LOG_AGENT_CONFIG_PATH`, which indicates the file path to Log Agent configuration. If this variable is not defined, Log Agent wouldn't start. 

> TODO: In the future, the controller will pass this configuration to Job Agent, which will then pass it to Log Agent. Change the APIs accordingly.

The Log Agent configuration file is a JSON file defines the following variables:

* `hanging_job_threshold_sec`:  [REQUIRED] The time in seconds to wait between logs before considering the job is hanging. 
* `slow_tolerance_times`: [OPTIONAL] The number of slow logs received before considering the job is slow, default to 1. 
* `rules` A list of rules for parsing the logs, each rule may have the following fields:
    * `name`: [OPTIONAL] Name of this metric
    * `pattern`: [REQUIRED] Regular expression pattern to match the logs. It may have one group to extract metric from the log (e.g. TFLOPs)
    * `type`: [OPTIONAL] value | str, default to str
    * `threshold`: [OPTIONAL] The threshold to compare with the extracted metric. If no extracted metric (i.e. regex group) and op, it would not be used
    * `op`: [OPTIONAL] Opterator used to compare threshold and metric, supported operators: `> | < | = | <= | >=`

See [/docker/log_config.json](../../../docker/log_config.json) for an example of Log Agent configuration. 

Log Agent runs as a separated threshold and should be `start()` and `stop()` with Job Agent. The `start()` method takes log file path as input, open the file, seek to the end of file and continue monitoring the new lines of the log file. PyTorch's distributed elastic agent writes logs to `<log_dir>/<rdzv_run_id>/attempt_<attempt>/<rank>/stdout.log`, where `<log_dir>/<rdzv_run_id>` is defined as `run_log_dir` and can be retrived from `log_specs._run_log_dir` *AFTER* starting the workers. The `--redirect` flag must be set properly to allow writing logs to file. 

The Log Agent reports four status by its `log_status` perperty:

1. `WAITING`: Waiting for the log agent to start or first log to come out
2. `HEALTHY`: The logs are within expectation
3. `SLOW`: The log metrics are out of expectation, indicating a slow job
4. `HANGING`: No matched log has been received for a long time, indicating a hanging job

The status changes from `HEALTHY` to `SLOW` when any of the rules evaluated to be False. The status changes to `HANGING` when no log is matched for `hanging_job_threshold_sec` seconds. For now, we allow the status to change back to `HEALTHY` as long as we receive new and healthy logs. 

