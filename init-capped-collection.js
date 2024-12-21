db = db.getSiblingDB("social_media");

db.createCollection("results", {
  capped: true,
  size: 5000,
  max: 5,
});

print('Capped collection "results" created with a maximum of 5 documents.');
