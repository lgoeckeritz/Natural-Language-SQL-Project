import json
from openai import OpenAI
import os
import sqlite3
from time import time

print("Running db_bot.py!")

fdir = os.path.dirname(__file__)
def getPath(fname):
    return os.path.join(fdir, fname)

# SQLITE
sqliteDbPath = getPath("aidb.sqlite")
setupSqlPath = getPath("setup.sql")
setupSqlDataPath = getPath("setupData.sql")

# Erase previous db
if os.path.exists(sqliteDbPath):
    os.remove(sqliteDbPath) 

sqliteCon = sqlite3.connect(sqliteDbPath) # create new db
sqliteCursor = sqliteCon.cursor()
with (
        open(setupSqlPath) as setupSqlFile,
        open(setupSqlDataPath) as setupSqlDataFile
    ):

    setupSqlScript = setupSqlFile.read()
    setupSQlDataScript = setupSqlDataFile.read()

sqliteCursor.executescript(setupSqlScript) # setup tables and keys
sqliteCursor.executescript(setupSQlDataScript) # setup tables and keys

def runSql(query):
    result = sqliteCursor.execute(query).fetchall()
    return result

# OPENAI
configPath = getPath("config.json")
print(configPath)
with open(configPath) as configFile:
    config = json.load(configFile)

openAiClient = OpenAI(
    api_key = config["openaiKey"],
    organization = config["orgId"]
)

def getChatGptResponse(content):
    stream = openAiClient.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )

    responseList = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            responseList.append(chunk.choices[0].delta.content)

    result = "".join(responseList)
    return result

# strategies TODO: put in my own single_domain_double_shot
commonSqlOnlyRequest = " Give me a sqlite select statement that answers the question. Only respond with sqlite syntax. If there is an error do not expalin it!"
strategies = {
    "zero_shot": setupSqlScript + commonSqlOnlyRequest,
    "single_domain_double_shot": (setupSqlScript + 
                   " How many unique people has Emma Watson appeard in photos with? " + 
                   "\nSELECT COUNT(DISTINCT pip.personID) AS unique_people_with_emma_watson\nFROM personInPhoto pip\nJOIN person p ON pip.personID = p.ID\nWHERE pip.photoID IN (\n    SELECT photoID FROM personInPhoto WHERE personID = (\n        SELECT ID FROM person WHERE firstName = 'Emma' AND lastName = 'Watson'\n    )\n)\nAND p.ID != (\n    SELECT ID FROM person WHERE firstName = 'Emma' AND lastName = 'Watson'\n);\n" +
                   commonSqlOnlyRequest)
}

questions = [ # TODO: put in my own questions: possible double shot is who is the best at taking group photos
    "How many people are in the database?",
    "How many photos in the Friends 2024 album were shot on a Samsung Galaxy S21?",
    "How many pictures did Bob Jones appear in?",
    "Who is the most popular?",
    "Who is the best at taking group photos?",
    "David lee and Emma watson are always involved in pictures of each other. If there is a picture of emma without david lee, that means that david took the picture. If there is a picture of david without emma, then emma took the picture. If both david and emma are in a picture, then david took the picture. Between david and emma, who took more pictures?",
    "How many unique people has Emma Watson appeard in photos with?"
]

def sanitizeForJustSql(value):
    gptStartSqlMarker = "```sql"
    gptEndSqlMarker = "```"
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]

    return value

for strategy in strategies:
    responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
    questionResults = []
    for question in questions:
        print(question)
        error = "None"
        try:
            sqlSyntaxResponse = getChatGptResponse(strategies[strategy] + " " + question)
            sqlSyntaxResponse = sanitizeForJustSql(sqlSyntaxResponse)
            print(sqlSyntaxResponse)
            queryRawResponse = str(runSql(sqlSyntaxResponse))
            print(queryRawResponse)
            friendlyResultsPrompt = "I asked a question \"" + question +"\" and the response was \""+queryRawResponse+"\" Please, just give a concise response in a more friendly way? Please do not give any other suggests or chatter."
            friendlyResponse = getChatGptResponse(friendlyResultsPrompt)
            print(friendlyResponse)
        except Exception as err:
            error = str(err)
            print(err)

        questionResults.append({
            "question": question, 
            "sql": sqlSyntaxResponse, 
            "queryRawResponse": queryRawResponse,
            "friendlyResponse": friendlyResponse,
            "error": error
        })

    responses["questionResults"] = questionResults

    with open(getPath(f"response_{strategy}_{time()}.json"), "w") as outFile:
        json.dump(responses, outFile, indent = 2)
            

sqliteCursor.close()
sqliteCon.close()
print("Done!")