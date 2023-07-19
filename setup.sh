# First check neo4j running 
echo "Check neo running ..."
result=$(neo4j status)
first_words=$(echo "$result" | awk '{print $1, $2, $3}')
# Check the result using an if statement
if [[ "$first_words" == "Neo4j is running" ]]; then
    echo "Neo4j is running."
else
    echo "Not running, starting"
    neo4j start
fi


