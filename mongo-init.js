db = db.getSiblingDB("cluster0");
db.createUser({
    user: "randomsandstrings",
    pwd: "randoms&str1ngs",
    roles: [{
        role: "dbOwner",
        db: "cluster0"
    }]
});
