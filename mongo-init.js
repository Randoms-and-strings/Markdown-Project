const database = process.env.MONGO_INITDB_DATABASE
const customUsername = process.env.CUSTOM_USERNAME
const customPassword = process.env.CUSTOM_PASSWORD

db = db.getSiblingDB(database);
db.createUser({
    user: customUsername,
    pwd: customPassword,
    roles: [{
        role: "dbOwner",
        db: database
    }]
});
