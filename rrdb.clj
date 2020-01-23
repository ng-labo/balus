(ns user (:require [net.cgrand.enlive-html :as html]))
(def asnum 16503)
(def radb-url (format "https://www.radb.net/query?advanced_query=1&keywords=as%d&-i=1&-i+option=origin" asnum))
(def html-text (slurp radb-url))
(def list-pre (-> html-text (html/html-snippet)(html/select [:pre])))
(defn proc [x]
    (second (clojure.string/split (first (clojure.string/split (first((first (x :content)) :content)) #"\n" )) #"\s+"))
)
(map proc list-pre)
