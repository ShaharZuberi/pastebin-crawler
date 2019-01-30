# pastebin-crawler



#Discussion:
1. What will happen if the link to the pasted bin will be changed? should we use a different uniqe key?
2. We import and save to the db before iterating to the next pasted bin with an intention to avoid data loss if failure occurs 
3. What will happen in case a first thread is stuck and a second one started to run after? in such a case duplicates will be written to the DB. such case could be handled in reading verification right before writing to db and removal of instance from the memory structure
4. we kept MAX_IN_MEMORY_PASTES attribute to keep a max length of objects in the memory just in case. All of the objects are written to the db anyway
5. I handled request exceptions and separated between an archive failure(WebCrawler) and a single pasted bin failure(PastedBin)
6. DB pastes filtering is done with one open-close for the entire pastes fetched