"""
@author: M. Bernt
"""


class tax:
    def __init__(self, nodepath, namepath, mergepath):
        self._tree = dict()
        self.__readtax(nodepath, namepath)
        self._merged = dict()
        self.__readmerge(mergepath)

    def __addname(self, name, lst):
        for lname in lst:
            if lname.lower() == name.lower():
                if name[0] == name[0].upper() and lname != name[0].upper():
                    lst.remove(lname)
                    lst.append(name)
                return
        lst.append(name)

    def __readtax(self, nodepath, namepath):
        """
        @param nodepath path containing the node file (nodes.dmp)
        @param namepath path containing the name file (names.dmp)
        @return A dict where key is the TAXID subject a list.
            The first field is the parent node
            The second field is the type of the node (kingdom,family...)
            The third field is a list of names for the node
                and the first name is the scientific name
        """

        # open the node file
        f = open(nodepath)
        # read the first line
        line = f.readline()
        # read until the empty line at the end
        while line.rstrip() != "":
            # tab seperadet format
            cols = [x.strip() for x in line.split("|")]
            # o objekt is TAXID
            # 2 objekt is over node
            # 4 objekt is the type of the node
            self._tree[int(cols[0])] = [int(cols[1]), cols[2], [""]]
            # read next line
            line = f.readline()
        f.close()

        # open the name file
        f = open(namepath)
        # read the first line
        line = f.readline()
        # read until the empty line at the end
        while line.rstrip() != "":
            # tab seperadet format
            cols = [x.strip() for x in line.split("|")]
            # 1 objekt is the name
            # 2 objekt is the type of name
            if (
                cols[3].strip() == "scientific name"
                and self._tree[int(cols[0])][2][0] == ""
            ):
                self._tree[int(cols[0])][2][0] = cols[1]
            else:
                self.__addname(cols[1], self._tree[int(cols[0])][2])
            # read next line
            line = f.readline()
        f.close()

    def __readmerge(self, mergpath):
        # open the merg file
        f = open(mergpath)
        # read the first line
        line = f.readline()
        # read until the empty line at the end
        while line.rstrip() != "":
            cols = [x.strip() for x in line.split("|")]
            # cols[0] old
            # cols[1] new
            self._merged[int(cols[0])] = int(cols[1])
            line = f.readline()

    def __get_id(self, iid):

        while iid not in self._tree:
            try:
                iid = self._merged[iid]
            except KeyError:
                raise Exception(
                    "Taxonomy Error %d not in parents and not in merged" % (iid)
                )

        return iid

    def gettaxway(self, taxid):
        """
        @param taxid the taxid of the spezies
        @return A list of node that is the way from spezies to root(first spezies)
            every node is a List: [taxid,rank,names]
        """

        # set the spezies as first element
        taxid = self.__get_id(taxid)
        taxway = [[taxid, self._tree[taxid][1], self._tree[taxid][2]]]
        # go from spezies to root
        while taxid != 1:
            taxid = self._tree[self.__get_id(taxid)][0]
            taxway.append([taxid, self._tree[taxid][1], self._tree[taxid][2]])

        return taxway
