# evol-aiq - API


#not in use
curl -H "Content-Type: application/json" -X POST http://localhost:5000/churn/v1/loadModel -d '{"model_name":"model","service_name": "service","model_version":"v1", "username":"admin", "password":"admin"}'

curl -H "Content-Type: application/json" -X POST http://localhost:5000/churn/v1/startTrain -d '{"service_name":"churn","algorithm":"1","overwrite_model":true,"hyper_parameters":{"max_depth":[3,4],"learning_rate":[0.01]},"username":"admin","password":"admin"}'
curl -H "Content-Type: application/json" -X POST http://localhost:5000/churn/v1/publishModel -d '{"run_id":"23", "username":"admin", "password":"admin"}'
curl -H "Content-Type: application/json" -X POST http://localhost:5000/churn/v1/predict -d '{"records":[{"feature_data":{"age":"10","data_usage":"high"},"identifier":"9830188417"},{"feature_data":{"age":"10","data_usage":"high"},"identifier":"9830188418"},{"feature_data":{"age":"10","data_usage":"high"},"identifier":"9830188419"}], "username":"admin","password":"admin"}'

 


# evol-aiq - data loader`

curl -X PUT "http://localhost:9200/aiq_subscriberprofile" \
-H "Content-Type: application/json" \
-d '{
  "mappings": {
    "properties": {
      "customerid":      { "type": "keyword" },
      "name":            { "type": "text" },
      "msisdn":          { "type": "keyword" },
      "activationdate":  { "type": "date", "format": "yyyy-MM-dd||epoch_millis" },
      "channelid":       { "type": "keyword" },
      "currentsegment":  { "type": "keyword" },
      "churnscore":      { "type": "float" }
    }
  }
}'


curl -X POST "http://localhost:9200/aiq_subscriberprofile/_bulk" \
-H "Content-Type: application/json" \
-d '
{ "index": {} }
{ "customerid": "CUST001", "name": "Rahul Sharma", "msisdn": "9876543210", "activationdate": "2024-07-15", "channelid": "CH_APP", "currentsegment": "SEG_PREMIUM", "churnscore": 12.50, "created_at": "2025-11-11 16:35:05", "updated_at": "2025-11-11 16:35:05" }
{ "index": {} }
{ "customerid": "CUST002", "name": "Priya Gupta", "msisdn": "9123456789", "activationdate": "2023-12-10", "channelid": "CH_RETL", "currentsegment": "SEG_REGULAR", "churnscore": 35.20, "created_at": "2025-11-11 16:35:05", "updated_at": "2025-11-11 16:35:05" }
{ "index": {} }
{ "customerid": "CUST003", "name": "Amit Verma", "msisdn": "9988776655", "activationdate": "2024-01-05", "channelid": "CH_DIR", "currentsegment": "SEG_NEW", "churnscore": 5.00, "created_at": "2025-11-11 16:35:05", "updated_at": "2025-11-11 16:35:05" }

select * from subscriberprofile WHERE updated_at < CURDATE() and churndate is null;
UPDATE subscriberprofile SET churndate = null,updated_at = CURDATE() - INTERVAL 2 DAY  where customerid ='CUST004';