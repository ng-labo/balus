(ns user (:require [net.cgrand.enlive-html :as html]))

(defn radb-url [asnum] (format "https://www.radb.net/query?advanced_query=1&keywords=as%d&-i=1&-i+option=origin" asnum))
;(defn radb-url [_] "localsample")

(defn list-pre [asnum] (-> (slurp (radb-url asnum)) (html/html-snippet)(html/select [:pre])))

(defn makeonemap [x]
  (reduce (fn [h [_ k v]](assoc h k v)) {} (re-seq #"(.+):\s+(.+)(\n|$)" x))
)
(defn proc [x]
  ;(clojure.string/split (first (clojure.string/split (first((first (x :content)) :content)) #"\n" )) #"\s+")
  ;(clojure.string/split (first((first (x :content)) :content)) #"\n" )
  (let [o (makeonemap (first((first (x :content)) :content)))]
     (if (get o "route" ) (println (format "%s:" (get o "route" ))))
     (if (get o "route6") (println (format "%s:" (get o "route6"))))
     (if (get o "descr" ) (println "    description:" (get o "descr") ))
     (if (get o "origin" ) (println "    asn:" (clojure.string/replace (get o "origin") #"AS" "" )))
     (println "    ignoreMorespecifics: false")
  )
)

(doall (map proc (list-pre 16503)))
