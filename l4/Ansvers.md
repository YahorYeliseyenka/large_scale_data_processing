# *Spark applications run as independent sets of processes on a cluster, coordinated by the SparkContext object in your main program (called the driver program).*

## why do we need to install Java, how pySpark works?
PySpark jest zbudowany na bazie Java API Sparka. Dane są przetwarzane w Pythonie i buforowane w JVM. W programie sterownika Python SparkContext używa Py4J do uruchamiania maszyny JVM i tworzenia JavaSparkContext. Py4J jest używany tylko w sterowniku do komunikacji lokalnej między obiektami Python i Java SparkContext; duże transfery danych są realizowane za pomocą innego mechanizmu.

## do we need to use Java 8?
Tak, ponieważ spark działa w Javie 8. Obsługa Java 7, Python 2.6 i starszych wersji Hadoop została usunięta ze Sparku.

## can we connect to an external cluster from python code?
Tak, korzystając z usługi **Apache Livy**, można połączyć się z zewnętrznym klastrem Spark z notebooków, aplikacji i interfejsów API.
https://docs.faculty.ai/how_to/spark/external_cluster.html

## can we deploy our python code to Spark cluster?
Tak, korzystając ze spark-submit

## how can we observe Spark jobs progress (Spark HTTP UI)?
Default: localhost:4040

## logistic regression vs linear regression
W regresji liniowej wynik (zmienna zależna) jest ciągły. Może mieć dowolną z nieskończonej liczby możliwych wartości.

W regresji logistycznej wynik (zmienna zależna) ma tylko ograniczoną liczbę możliwych wartości.

## multi-class vs multi-label
Różnica między klasyfikacją wieloklasową a klasyfikacją z wieloma etykietami polega na tym, że w przypadku problemów obejmujących wiele klas klasy wykluczają się wzajemnie, podczas gdy w przypadku problemów z wieloma etykietami każda etykieta reprezentuje inne zadanie klasyfikacyjne, ale zadania są w jakiś sposób powiązane.

## what is RDD
resilient distributed dataset (RDD) - odporny, rozproszony zestaw danych (RDD), czyli zbiór elementów podzielonych na węzły klastra, na których można równolegle pracować.
Niezmienna kolekcja obiektów, którą używa spark w celu zwięszenia prędkości przetwarzania operacji MapReduce.
https://spark.apache.org/docs/latest/rdd-programming-guide.html

## what is DataFrame
DataFrame to zestaw danych zorganizowany w nazwane kolumny. Koncepcyjnie jest odpowiednikiem tabeli w relacyjnej bazie danych lub ramce danych w R / Pythonie, ale z bogatszymi optymalizacjami pod maską.

## what is DataSet
Zestaw danych to rozproszony zbiór danych. Zestaw danych to nowy interfejs dodany do platformy Spark 1.6, który zapewnia zalety RDD (mocne pisanie, możliwość korzystania z zaawansowanych funkcji lambda) z zaletami zoptymalizowanego silnika wykonywania Spark SQL.

## how Spark generally works (master, worker)

## Spark stack (SQL, ML, GraphX etc.)
SQL - 

streaming - manipulacja strumieniami danych na żywo.

MLlib - wbudowana biblioteka do uczenia maszynowego

GraphX - to wbudowany interfejs API do przetwarzania wykresów służący do manipulowania wykresami

SparkR - jest w rzeczywistości pakietem R, który zapewnia powłokę R do wykorzystania rozproszonego silnika obliczeniowego Sparka.

https://subscription.packtpub.com/book/big_data_and_business_intelligence/9781785885655/1/ch01lvl1sec11/the-spark-stack#:~:text=Spark%20is%20a%20general%2Dpurpose,to%20leverage%20its%20core%20engine.

## shuffling
http://www.lifeisafile.com/All-about-data-shuffling-in-apache-spark/#:~:text=Shuffling%20is%20a%20process%20of,of%20data%20transfer%20between%20stages.
to proces przesyłania danych między etapami / partycjami.

## reduceByKey vs groupByKey
Unikaj groupByKey i zamiast tego użyj removeByKey lub connectByKey.

groupByKey tasuje wszystkie dane, co jest powolne.

RedukcjaByKey tasuje tylko wyniki subagregacji w każdej partycji danych.