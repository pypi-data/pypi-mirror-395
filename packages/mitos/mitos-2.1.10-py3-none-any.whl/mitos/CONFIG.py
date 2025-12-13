"""
@author: M. Bernt

defines:
logger
    the main log.


dbfill:
    TRANSLATIONFILEPATH: path to translation config file for GenBank parsing
    IGNOREDGENBANKFEATURES: featurestypes, which are ignored, when genbank data is inserted in db
    ASFEATURES: featuretype, which are treated as assigned sequences

uassearch:
    SSEARCH: path to the ssearch executable from the fasta package and parameters
    UASEARCHMINLEN: minimal length of the uas/ovl (only uas/ovl >= minlen are taken into account)
    UASSEARCHFOR: list of elements to search for (e.g. uas, ols)

lalign:
    LALIGNSEPARATINGSTRING: string, separating records in lalign-output


misc:
    TMPDIR: directory for temporary files

Meaning of activation code:
0 : current version
1 : deactivated, marked as deleted
2 : deactived, marked for merging

"""

# the root of the mtdb project
MTDB = "/home/maze/workspace/mtdb/"
# the src folder of the mtdb project
SRCPATH = MTDB + "src/"
# the data folder (containing featureProt...) of the mtdb project

#######################################################################
# WEBSERVER
#######################################################################

# switch server maintenance mode
# False: no maintenance = normal mode
# a string that should give the date and time when MITOS is expected back online
MAINTENANCE = False
# MAINTENANCE = "27. May 2013 Lunchtime (German time)"

# that the path where the sequences are processed
# - the queue client works in this directory
# WRKPATH = PROJECTPATH + "work/"
WRKPATH = "/var/www/mitos-output/"

# the path where:
# - the webserver stores the jobs
# - the queue is running (i.e. the queue takes jobs from here and puts the results there)
TOMCATPATH = "/var/www/mitos-output/"

# the url of mitos webserver: url+path (without http)
WEBPATH = "mitos2.bioinf.uni-leipzig.de"
# mailserver to be used
EMAILSERVER = "bierdepot.bioinf.uni-leipzig.de"
# webserver souce directory (text messages ...)
MITOSPATH = SRCPATH + "webserver/"

# mitos maximum sequence size
MITOS_MAXSEQSIZE = 1000000
MITOS_MINSEQSIZE = 50

# mitos maximum number of sequences per multifasta upload
MITOS_MAXNRSEQ = 10000

# add html code for tracking here will be inserted in all but the wait page
MITOS_TRACKING_CODE = """
<!-- Piwik -->
<script type="text/javascript">
var pkBaseURL = (("https:" == document.location.protocol) ? "https://piwikmitos.bioinf.uni-leipzig.de/" : "http://piwikmitos.bioinf.uni-leipzig.de/");
document.write(unescape("%3Cscript src='" + pkBaseURL + "piwik.js' type='text/javascript'%3E%3C/script%3E"));
</script><script type="text/javascript">
try {
var piwikTracker = Piwik.getTracker(pkBaseURL + "piwik.php", 2);
piwikTracker.trackPageView();
piwikTracker.enableLinkTracking();
} catch(err) {}
</script><noscript><p><img src="http://piwikmitos.bioinf.uni-leipzig.de/piwik.php?idsite=2" style="border:0" alt="" /></p></noscript>
<!-- End Piwik Tracking Code -->
"""

MITOS_CONTACTMAIL = "mitos@bioinf.uni-leipzig.de"
MITOS_SENDMAIL = "mitos-donotreply@bioinf.uni-leipzig.de"

# get copy "save" email coding from MITOS_CONTACTMAIL
# js encode
jsmail = MITOS_CONTACTMAIL.split("@")
jsmail[0] = "%" + "%".join("{0:x}".format(ord(c)) for c in jsmail[0])  # hex with %
jsmail[1] = (
    "&#x" + ";&#x".join("{0:x}".format(ord(c)) for c in jsmail[1]) + ";"
)  # hex as in html
# html encode
htmlmail = MITOS_CONTACTMAIL.split("@")
htmlmail[0] = (
    "&#x" + ";&#x".join("{0:x}".format(ord(c)) for c in htmlmail[0]) + ";"
)  # hex
htmlmail[1] = "&#" + ";&#".join("{0}".format(ord(c)) for c in htmlmail[1]) + ";"  # ord

MITOS_CONTACTMAILCRYPT = """<script type=\'text/javascript\'>
var pref = \'&#109;a\' + \'i&#108;\' + \'&#116;o\';
var attribut = 'hr' + 'ef' + '=';
var first = '{jsmaila}';
var at = '%40';
var last = '{jsmailb}';
var first2 = '{htmlmaila}';
var at2 = '&#x40;';
var last2 = '{htmlmailb}';
document.write('<a ' + attribut + '\\'' + pref + ':' + first + at + last + '\\'>');
document.write(first2 + at2 + last2);
document.write('</a>');
</script>
<noscript><div style='display:none; '>are-</div><div style='display:inline; '>{htmlmaila}</div> <div style='display:none; '>-xya34</div><div style='display:inline; '>[at]</div> <div style='display:none; '>ddks-</div> <div style='display:inline; '>{htmlmailb}</div></noscript>
""".format(
    jsmaila=jsmail[0], jsmailb=jsmail[1], htmlmaila=htmlmail[0], htmlmailb=htmlmail[1]
)
