// https://medium.com/faun/managing-mongodb-on-docker-with-docker-compose-26bf8a0bbae3

db.createUser(
    {
        user : "admin",
        pwd : "admin",
        roles : [
            {
                role : "readWrite",
                db : "dbsubmissions"
            }
        ]
    }
);