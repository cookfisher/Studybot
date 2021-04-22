
# active the rasa. 
$ conda activate rasa

# run actions server. have to do the server running, otherwise it shows error
$ rasa run actions

(rasa) D:\rasa>rasa run actions
2021-04-20 21:45:20 INFO     rasa_sdk.endpoint  - Starting action endpoint server...
2021-04-20 21:45:20 INFO     rasa_sdk.executor  - Registered function for 'action_person_info'.
2021-04-20 21:45:20 INFO     rasa_sdk.endpoint  - Action endpoint is up and running on http://localhost:5055

$ d:
$ cd rasa
$ rasa init
$ rasa train
$ rasa shell