# ipulse_shared_data_eng
Shared Data Engineering Code for ipulse platform, especially for Oracle module


### Collectors i.e. Pipelinemon

Collectors are smart Objects which are added to long running functions or pipelines for which we want to collect an overall number of successes, notices, warnings or errors. 

We can wait until the full pipeline is finished in order to write off a single Summary file from a Collector, or we can attach to it a logger, which will be reporting major status along the journey, which is often times better. Because if a function crashes midway through , all logs will be lost, and it would be hard to investigate if anythign has bee persisted and has to be rolled back. THis will require a lot of manual effort to recollect.

Pipelinemon , short of Pipeline Monitoring system is a type of very powerful Collector which Russlan created specifically for Pulse Data Engineering pipelines.

Pipelinemon writes all observation logs to Google CLoud Logging, and you have to setup a Log Sink (Router) which will send the Pipelinemon's observation logs to BigQuery. 

Great thing about Pipelinemin is its "context" keeping feature.



### Utils : Schema Checkers , Cloud Utils ( save file to cloud storage etc. for GCP, AWS, Azure etc.) , local files utils etc.


