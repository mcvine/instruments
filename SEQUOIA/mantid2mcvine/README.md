# Convert SEQ mantid IDF

Inputs
* run.py
* SEQ_virtual_Definition_12292017.xml

Run:

  $ python run.py

Outputs
* SEQ_virtual_12292017_mcvine.xml: mcvine IDF
* SEQ_virtual_template_12292017.nxs: template NXS file
* SEQ_virtual.yml: serialized instrument model that will be used in detector sim and nxs generation

Next,
* move SEQ_virtual_12292017_mcvine.xml, SEQ_virtual_template_12292017.nxs, SEQ_virtual.yml to SEQUOIA python subpackage,
  copy SEQ_virtual_Definition_12292017.xml to SEQUOIA python subpackage,
  and make sure *.xml, *.nxs, and *.yml are patterns that will be installed (CMakeLists.txt)
* create install_mantid_IDF.py in SEQUOIA python subpackage
* change SEQUOIA.applications Neutrons2Events and Events2Nxs