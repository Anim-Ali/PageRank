# PageRank
Implementation of PageRank (PR) algorithm, which is one of the algorithms used by Google Search to rank web pages in their search engine results.


## How to Run 

 Clone the repo
 ```sh
 git clone https://github.com/Anim-Ali/PageRank
 ```
 The program expects name of a directory of a corpus of web pages as a command-line argument. 
 
 Three directories with web pages (corpus) are in project folder.
 
 Each corpus can be ranked by giving the name of the corpus as an argument
 
 Move into the project directory in terminal and run the following commands
 ```sh
 python pagerank.py corpus0
 ```
 ```sh
 python pagerank.py corpus1
 ```
 ```sh
 python pagerank.py corpus2
 ```
 "PageRank Results from Sampling" shows results of page rankings by sampling pages from a Markov Chain random surfer.

 "PageRank Results from Iteration" shows results of page rankings by iteratively applying the PageRank formula.