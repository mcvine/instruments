import numpy as np

#Creation of the Bank Detectors Positions and Rotation angles#
#Automatic generation of the positions of the bank detectors for CHESS#

log_filename = "/SNS/users/gqs/notebooks/Desktop/AMATERAS_detector_test.xml"
with open(log_filename,'w') as file:

    file.write(' <!--Created by Gabriele Sala-->\n')
    file.write(' <defaults>\n')
    file.write('   <length unit="metre"/>\n')
    file.write('   <angle unit="degree"/>\n')
    file.write('   <reference-frame>\n')
    file.write('     <along-beam axis="z"/>\n')
    file.write('     <pointing-up axis="y"/>\n')
    file.write('     <handedness val="right"/>\n')
    file.write('   </reference-frame>\n')
    file.write(' </defaults>\n')
    file.write('\n')
    file.write(' <!--SOURCE AND SAMPLE POSITION-->\n')
    file.write(' <component type="moderator">\n')
    file.write('   <location z="-30.0"/>\n')
    file.write(' </component>\n')
    file.write(' <type is="Source" name="moderator"/>\n')
    file.write(' <component type="sample-position">\n')
    file.write('   <location x="0.0" y="0.0" z="0.0"/>\n')
    file.write(' </component>\n')
    file.write(' <type is="SamplePos" name="sample-position"/>\n')
    file.write('\n')
    file.write(' <!--MONITORS-->\n')
    file.write(' <component idlist="monitors" type="monitors">\n')
    file.write('   <location/>\n')
    file.write(' </component>\n')
    file.write(' <type name="monitors">\n')
    file.write('   <component type="monitor">\n')
    file.write('     <location name="monitor1" z="-29.9"/>\n') # These needs to be modified ONCE you have the final dimensions
    file.write('     <location name="monitor2" z="-15.8"/>\n') # These needs to be modified ONCE you have the final dimensions
    file.write('     <location name="monitor3" z="-1.6"/>\n') # These needs to be modified ONCE you have the final dimensions
    file.write('   </component>\n')
    file.write(' </type>\n')
    file.write('\n')
    file.write('\n')
    file.write('\n')
    
    #Left pack of Detecors facing the beam 
    radiusl=4.0
    
    #anglerange=np.arange(-39.5,140.,3.14)
    anglerange=np.array([-39.4, -36.26, -33.12, -29.98, -26.41, -23.27, -20.13, -16.99,-13.42, -10.28, -7.14, -4., -0.43, 2.71, 5.85, 8.99, 12.56, 15.7, 18.84, 21.98, 25.55, 28.69, 31.83, 34.97, 38.54, 41.68, 44.82, 47.96, 51.53, 54.67, 57.81, 60.95, 64.52, 67.66, 70.8, 73.94, 77.51, 80.65, 83.79, 86.93, 90.5, 93.64, 96.78, 99.92, 103.49, 106.63, 109.77, 112.91, 116.48, 119.62, 122.76, 125.9, 129.47, 132.61, 135.75, 138.89])
    anglel=np.radians(anglerange[::-1]-100.)
    bank0l=0

    for ii in range(0,len(anglel)):
        xl=radiusl*np.sin(anglel[ii])
        zl=radiusl*np.cos(anglel[ii])
        if anglel[ii] < np.radians(156.0): # This is the shadow angle for back-sattering #
            bank0l+=1
            file.write('<type name="bank'+str(bank0l)+'">\n')
            file.write('  <component type="eightpack">\n')
            file.write('    <location x="'+str(xl)+'" y="0.305" z="'+str(zl)+'">\n')
            file.write('      <rot axis-x="0" axis-y="1" axis-z="0" val="'+str(180.0+np.degrees(anglel[ii]))+'">\n')
            file.write('      </rot>\n')
            file.write('    </location>\n')
            file.write('  </component>\n')
            file.write('</type>\n')
    
    #for ii in range(1,129,1):
    #    pos = -0.554296875 + ii*(1.1/128.)
    #    file.write('<location name="pixel{0}" y="{1}"/>\n'.format(ii,pos))
    
    #for ii in range(1,129,1):
    #    pos = -0.403125 + ii*(0.8/128.)
    #    file.write('<location name="pixel{0}" y="{1}"/>\n'.format(ii,pos))
    '''
    #Short SANS pack of Detecors facing the beam 
    radiusl=6.5
    
    #anglerange=np.arange(-3.9,6.,1.4)
    anglerange=np.linspace(-3.5,5.5,10)
    anglel=np.radians(anglerange[::-1])
    bank0l=122

    for ii in range(0,len(anglel)):
        xl=radiusl*np.sin(anglel[ii])
        zl=radiusl*np.cos(anglel[ii])
        if anglel[ii] < np.radians(156.0): # This is the shadow angle for back-sattering #
            bank0l+=1
            file.write('<type name="bank'+str(bank0l)+'">\n')
            file.write('  <component type="eightpack-short">\n')
            file.write('    <location x="'+str(xl)+'" y="0.0" z="'+str(zl)+'">\n')
            file.write('      <rot axis-x="0" axis-y="1" axis-z="0" val="'+str(180.0+np.degrees(anglel[ii]))+'">\n')
            file.write('      </rot>\n')
            file.write('    </location>\n')
            file.write('  </component>\n')
            file.write('</type>\n')
    '''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

