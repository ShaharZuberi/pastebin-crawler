# pastebin-crawler
Welcome to Pastebin.com crawler

#### Automatic execution
Run the docker image.

#### Manual python execution
##### Installation
```bash
$ pip install arrow==0.13.0
$ pip install beautifulsoup4==4.7.0
$ pip install requests==2.21.0
$ pip install tinydb==3.12.2
``` 

##### Execution
```bash
$ python sample.py
``` 


## Discussion:
1. What will happen if the link to the pasted bin will be changed? should we use a different uniqe key?
2. We import and save to the db before iterating to the next pasted bin with an intention to avoid data loss if failure occurs 
3. What will happen in case a first thread is stuck and a second one started to run after? We filtered our the saved keys before fetching them. During the fetching time a different thread may write that key to the db. if no lock is implemeneted then duplicates will be written to the DB. If a lock is implemeneted, then we will have to lock the db and then check last time if that key exist before inserting. (That is basically the tradeoff)
4. we kept MAX_IN_MEMORY_PASTES attribute to keep a max length of objects in the memory just in case. All of the objects are written to the db anyway
5. I handled request exceptions and separated between an archive failure(WebCrawler) and a single pasted bin failure(PastedBin) inclding fetchnig raw data
6. DB pastes filtering is done with one open-close command for the entire pastes fetched.