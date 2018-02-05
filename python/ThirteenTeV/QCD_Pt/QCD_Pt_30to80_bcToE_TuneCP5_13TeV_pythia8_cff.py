import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
	maxEventsToPrint = cms.untracked.int32(1),
	pythiaPylistVerbosity = cms.untracked.int32(1),
	filterEfficiency = cms.untracked.double(0.00020),
	pythiaHepMCVerbosity = cms.untracked.bool(False),
	comEnergy = cms.double(13000.0),

	crossSection = cms.untracked.double(1.27298e+09),

	PythiaParameters = cms.PSet(
            pythia8CommonSettingsBlock,
            pythia8CP5SettingsBlock,
	    processParameters = cms.vstring(
			'HardQCD:all = on',
			'PhaseSpace:pTHatMin = 30  ',
			'PhaseSpace:pTHatMax = 80  ',
	    ),
            parameterSets = cms.vstring('pythia8CommonSettings',
                                        'pythia8CP5Settings',
                                        'processParameters',
                                        )
	)
)

genParticlesForFilter = cms.EDProducer("GenParticleProducer",
    saveBarCodes = cms.untracked.bool(True),
    src = cms.InputTag("generator"),
    abortOnUnknownPDGCode = cms.untracked.bool(False)
)

bctoefilter = cms.EDFilter("BCToEFilter",
                           filterAlgoPSet = cms.PSet(eTThreshold = cms.double(10),
                                                     genParSource = cms.InputTag("genParticlesForFilter")
                                                     )
                           )

configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('\$Revision$'),
    name = cms.untracked.string('\$Source$'),
    annotation = cms.untracked.string('b/c->e filtered QCD pthat 30to80 GeV, 13 TeV, TuneCP5')
)

# add your filters to this sequence
ProductionFilterSequence = cms.Sequence(generator * (genParticlesForFilter + bctoefilter ))



