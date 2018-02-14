# -*- Python -*-
#

from . import mantid2mcvine # make sure mantid IDF is there


# constants
L_Beam = 19.9                  # Moderator to neutron recorder distance.
                               # This has to match the neutron recorder position .../etc/sequoia_moderator2sample/sequoia_moderator2sample.pml

L_BeamEnd2Sample = 0.15        # End of beam to sample. This is used in mcvine.workflow.cli
L_Mod2Sample = 19.9 + 0.15     # Moderator sample distance. This has to match the mantid IDF and the mantid template nexus file.
                               # SEQ_virtual_Definition_12292017.xml and SEQ_virtual_template_12292017.nxs

# End of file 
