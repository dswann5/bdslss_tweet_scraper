conn = new Mongo();
db = conn.getDB("tweet_database");
db.tweets.find({},{ _id: 1, id: 1, text: 1, entities: 1, user: 1}).forEach(
    function(doc){
        db.filtered.insert(doc)
    }
);
