""" complete example of using MetaMap api """
import sys
import os
import string
from jpype import *
# sys.path.append("D:\Kuangyichen\public_mm\src\javaapi\dist\MetaMapApi.jar")
# sys.path.append("D:\Kuangyichen\public_mm\src\javaapi\dist\prologbeans.jar")

# from se.sics.prologbeans import PrologSession
# from gov.nih.nlm.nls.metamap import MetaMapApi, MetaMapApiImpl, Result

jarpath = os.path.join(os.path.abspath('.'), \
                       "D:\Kuangyichen\public_mm\src\javaapi\dist\MetaMapApi.jar")
startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % jarpath)
TA = JPackage('MetaMapApi').MetaMapApiImpl

class testapi:
    def __init__(self):
        self.api = TA()

    def process(self, inputtext):
        return self.api.processCitationsFromString(inputtext)

    def display_aas(self, result, output=sys.stdout):
        aalist = result.getAcronymsAbbrevs()
        if len(aalist) > 0:
            for e in aalist:
                output.write('Acronym: %s\n' % e.getAcronym())
                output.write('Expansion: %s\n' % e.getExpansion())
                output.write('Count list: %s\n' % e.getCountList())
                output.write('CUI list: %s\n' % e.getCUIList())
        else:
            output.write('None.')

    def display_negations(self, result, output=sys.stdout):
        neglist = result.getNegations()
        if len(neglist) > 0:
            for e in neglist:
                output.write("type: %s, " % e.getType())
                output.write("Trigger: %s: [ " % e.getTrigger())
                for pos in  e.getTriggerPositionList():
                    output.write('%s,' % pos)
                output.write('], ')
                output.write("ConceptPairs: %s: [ " % e.getConceptPairList())
                for pair in  e.getTriggerPositionList():
                    output.write('%s,' % pair)
                output.write('], ')
                output.write("Concept Positions: %s: [ " % e.getConceptPositionList())
                for pos in  e.getTriggerPositionList():
                    output.write('%s,' % pos)
                output.write(']\n')

    def display_utterances(self, result, display_pcmlist=False, output=sys.stdout):
        for utterance in result.getUtteranceList():
            output.write("Utterance:\n")
            output.write(" Id: %s\n" % utterance.getId())
            output.write(" Utterance text: %s\n" % utterance.getString())
            output.write(" Position: %s\n" % utterance.getPosition())
            if display_pcmlist:
                for pcm in utterance.getPCMList():
                    output.write("Phrase:\n")
                    output.write(" text: %s\n" % pcm.getPhrase().getPhraseText())
                    output.write("Candidates:\n")
                    for ev in pcm.getCandidates():
                        output.write(" Candidate:\n")
                        output.write("  Score: %s\n" % ev.getScore())
                        output.write("  Concept Id: %s\n" % ev.getConceptId())
                        output.write("  Concept Name: %s\n" % ev.getConceptName())
                        output.write("  Preferred Name: %s\n" % ev.getPreferredName())
                        output.write("  Matched Words: %s\n" % ev.getMatchedWords())
                        output.write("  Semantic Types: %s\n" % ev.getSemanticTypes())
                        output.write("  is Head?: %s\n" % ev.isHead())
                        output.write("  is Overmatch?: %s\n" % ev.isOvermatch())
                        output.write("  Sources: %s\n" % ev.getSources())
                        output.write("  Positional Info: %s\n" % ev.getPositionalInfo())
                    output.write("Mappings:\n")
                    for map in pcm.getMappings():
                        output.write(" Map Score:% s\n" % map.getScore())
                        for mapev in map.getEvList():
                            output.write("  Score: %s\n" % mapev.getScore())
                            output.write("  Concept Id: %s\n" % mapev.getConceptId())
                            output.write("  Concept Name: %s\n" % mapev.getConceptName())
                            output.write("  Preferred Name: %s\n" % mapev.getPreferredName())
                            output.write("  Matched Words: %s\n" % mapev.getMatchedWords())
                            output.write("  Semantic Types: %s\n" % mapev.getSemanticTypes())
                            output.write("  is Head?: %s\n" % mapev.isHead())
                            output.write("  is Overmatch?: %s\n" % mapev.isOvermatch())
                            output.write("  Sources: %s\n" % mapev.getSources())
                            output.write("  Positional Info: %s\n" % mapev.getPositionalInfo())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: %s terms' % sys.argv[0])
        exit(1)
    else:
        inst = testapi()
        resultList = inst.process(string.join(sys.argv[1:]))
        for result in resultList:
            inst.display_aas(result)
            inst.display_negations(result)
            inst.display_utterances(result, display_pcmlist=True)
