import cluster_db
import filter_db
import conditioning
import kmeans

import sys
mode = int(sys.argv[1])

if mode == 0:
    # Process raw Mnemosyne logs
    print "Processing logs..."
    filter_db.create_newdb()
    filter_db.create_regressiondb()
    filter_db.create_discretizeddb()
    cluster_db.create_userdb()
    print "Done processing logs."
elif mode == 1:
    # Run kmeans clustering
    kmeans.run_kmeans(5)
elif mode == 2:
    # Run conditioning
    conditioning.run_conditioning_disc(conditioning.ACQ_GROUP, 5)
else:
    print "No mode %s" % mode
    exit(1)

