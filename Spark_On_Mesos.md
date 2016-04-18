**Spark Cluster on Mesos (GCE)**


*Please note: The VAST majority of this material is taken from Paco Nathan's excellent blog post of 09-10-2014.  http://ceteri.blogspot.com/2014/09/spark-atop-mesos-on-google-cloud.html  The original post spun up a v1.0.1 Scala Spark instance.  I have modified the procedure to show how to run pySpark as well as SparkR using Spark 1.4.1.   I also added a section to cut back the console messaging.  Thom Rogers 08-31-2015* 


1.  **Create project in Google Cloud Platform**

    1.  [https://console.developers.google.com/project](https://console.developers.google.com/project)

    2.  Once created, be sure to click on the Billing link, enable
        billing and arrange payment details.



2.  **Launch a Mesosphere cluster**

    1.  [https://google.mesosphere.io/](https://google.mesosphere.io/)

    2.  click the +New Cluster button to get started

    3.  choose a configuration for your Mesosphere cluster

    4.  provide both a public SSH key and a GCP project identifier to
        launch a cluster

        1.  my SSH key at C:\\Users\\Les Paul\\.ssh\\github\_rsa.pub

        2.  GCP project identifier from Google Dev Console

    5.  Click the shiny purple Launch Cluster button. *It will take a
        few minutes for those VMs to launch and get configured*



3.  **Set up Spark**

    1.  SSH into Mesos Master

        1.  Check your Mesosphere cluster console in the browser, and
            scroll down to the Topology section. There should be one VM
            listed under the Master section, with both internal and
            external IP addresses shown for it. Copy the internal IP
            address for the Mesos master to clipboard, and make a note
            about its external IP address.

        2.  login through SSH to the Mesos master by logging in through
            the GCP console

            1.  click on the project link (see \#1 above)

            2.  click on the **Compute** section

            3.  click on the **Compute Engine** subsection

            4.  click on the **VMs instances** subsection

                1.  find your Mesos master, based on its external IP
                    address

                2.  click on the SSH button for the master to launch a
                    terminal window in your browser

    2.  Load Apache Spark - *Downloads at
        http://spark.apache.org/downloads.html . For this example we’ll
        use the latest Apache Spark distribution (1.4.1), “Pre-built for
        Hadoop 2.6 and later”.*

        1.  wget
            [http://apache.cs.utah.edu/spark/spark-1.4.1/spark-1.4.1-bin-hadoop2.6.tgz](http://apache.cs.utah.edu/spark/spark-1.4.1/spark-1.4.1-bin-hadoop2.6.tgz)

        2.  tar xzvf spark-1.4.1-bin-hadoop2.6.tgz

    3.  Configure variables

        1.  Logging – as shipped, the default logging-to-console level
            is set to INFO which is somewhat verbose. Many users find
            this distracting and instead, set this to WARN for less
            verbose console messaging.

            1.  cd spark-1.4.1-bin-hadoop2.6/conf

            2.  cp log4j.properties.template log4j.properties

            3.  edit the line “log4j.rootCategory=INFO, console” to read
                “log4j.rootCategory=WARN, console “. After editing, save
                the file in the conf directory.

        2.  Set environment variables

            1.  cd spark-1.4.1-bin-hadoop2.6/conf

            2.  cp spark-env.sh.template spark-env.sh

            3.  echo "export
                MESOS\_NATIVE\_LIBRARY=/usr/local/lib/libmesos.so" \>\>
                spark-env.sh

            4.  echo "export
                SPARK\_EXECUTOR\_URI=http://apache.cs.utah.edu/spark/spark-1.4.1/spark-1.4.1-bin-hadoop2.6.tgz"
                \>\> spark-env.sh

            5.  cp spark-defaults.conf.template spark-defaults.conf

            6.  echo "spark.mesos.coarse=true" \>\> spark-defaults.conf

            7.  cd ..

    4.  Launch Spark – version 1.4.1 ships with 4 different APIs
        available (Scala, Java, Python, R). API selection is invoked
        using start-up command, executed from the
        “spark-1.4.1-bin-hadoop2.6” directory.

        1.  Scala & Java

./bin/spark-shell --master mesos://\$MESOS\_MASTER:5050



2.  Python

./bin/pyspark --master mesos://\$MESOS\_MASTER:5050



3.  R

./bin/sparkR –master mesos://\$MESOS\_MASTER:5050



4.  Verify cluster operation – after launching Spark (pySpark), at the
    prompt, enter these two lines (these are for the pySpark API):

    1.  data = range(1,10001)

    2.  sc.parallelize(data).sum()

the commands above create a list of 10,000 consecutive numbers and
parallelizes them across the cluster as an RDD. It then sums them
together and prints the result, **5,000,5,000**to the screen


