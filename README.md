









<!-- Setting up AWS CodePipeline

You can configure AWS CodePipeline to use GitHub as your source code.

You need to create your GitHub Repository first.

Then-

1. Visit AWS console, Create pipeline, give your pipeline a name. ie. Perhap
2. Choose GitHub as your Source Provider
3. Click Connect to GitHub
4. Grant Access and Authorize Application
5. Choose Repository and Branch
6. Click Next Step
7. Choose Build Provider- No Build --Click Next Step
8. Choose Deployment Provider- AWS CloudFormation
  - Action Mode - Create or update a stack
  - Stack Name




  Kinesis-

  One Shard can support up to 5 transactions per second for reads, up to a maximum total data read rate of 2 MB per second and up to 1,000 records per second for writes, up to a maximum total data write rate of 1 MB per second.

  This set up will enable one shard on the Kinesis Stream. If you need more, you will also need to add a Partition Key in the lambda that adds the event to the Kinesis Stream
    Something like This
      kinesis.put_record(StreamName="perhap",
        Data=json.dumps(item),
        PartitionKey=str(item["domain"]) -->
