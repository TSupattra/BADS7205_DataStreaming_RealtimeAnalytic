
# WordCount Harry on Spark on local machine  

 ***1. Start a kafker cluster (zoo + brokers)***    
     Double click on 1_start_cluster.bat

 ***2. Create a topic***    
     Double click on 2_create_test_topics.bat

 ***3. Download the "spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar" and "kafka_spark_wordcount_Harry.py" file from this github to drive C:\ in same folder***


 ***4. Setup and run Spark on local machine*** 
 
  ```
  spark-submit --jars C:\spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar kafka_spark_wordcount_Harry.py

  ```

 ***5. Run Prosucer to send Text 1 line/secound***    
     Run producer-Harrytext_pyspark.py in command prompt 

