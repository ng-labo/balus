(ns user (:require [net.cgrand.enlive-html :as html]))

(defn radb-url [asnum] (format "https://www.radb.net/query?advanced_query=1&keywords=as%d&-i=1&-i+option=origin" asnum))
;(defn radb-url [_] "localsample")

(defn list-pre [asnum] (-> (slurp (radb-url asnum)) (html/html-snippet)(html/select [:pre])))

(defn parse-content [x]
  (reduce (fn [h [_ k v]](assoc h k v)) {} (re-seq #"(.+):\s+(.+)(\n|$)" x))
)

(defn create-raw-map [x]
  (map (fn [y] (parse-content (first((first (y :content)) :content)))) x)
)
(defn ip-map [x]
  (reduce (fn [h o]
    (cond
      (get o "route") (assoc h (get o "route") o)
      (get o "route6") (assoc h (get o "route6") o)
      :else h))
    {} x)
)
(defn print-list [x]
  (map (fn [[k v]]
        (println (format "%s:" k))
        (println "    description:" (get v "descr"))
        (println "    asn:" (clojure.string/replace (get v "origin") #"AS" ""))
        (println "    ignoreMorespecifics: false")
        (println "    ignore: false")
  ) x)
)

(doall (print-list (ip-map (create-raw-map (list-pre 9370)))))
(doall (print-list (ip-map (create-raw-map (list-pre 9371)))))
(doall (print-list (ip-map (create-raw-map (list-pre 7684)))))
