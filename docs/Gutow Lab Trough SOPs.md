# Langmuir Trough Standard Operating Procedures for the Gutow Lab
## Initialization
1. Check that recirculating temperature controller is connected to the 
   trough. Then turn it on and verify that the temperature is set to what 
   you want. Stabilization time is about 20 minutes for temperatures near 
   room temperature.
2. Turn on power to the trough.
3. Open a terminal and navigate to the `Trough` directory of the user 
   `Trough`.
4. Activate the trough python environment `pipenv shell`
5. Launch Jupyter Lab `jupyter lab`.
6. Within Jupyter Lab create a new folder for the Day. Name it something 
   like "DescriptiveWord_MMM_DD_YYYY", where MMM = three letter month 
   abbreviation, DD = day of the month and YYYY = the year.
7. Open the folder by clicking on it.
8. Open a new Notebook. Give it a descriptive name.
9. In the first cell run the command `import Trough_GUI`. If the trough has 
   not been started in the last 12 hours this will take a while as it checks 
   the motor calibration for moving the barriers.

## Checking Trough and Subphase Cleanliness
**This need to be done before each experiment.**
1. We usually use high-purity water as the subphase. Primarily this is 
   18+ M&Omega; de-ionized water mixed with KMnO<sub>4</sub> and redistilled.
   Depending on the status of the water polishers, it is sometimes possible 
   to use 18+ M&Omega; water from these directly.
2. If the trough is already filled with subphase (1 - 1.5 mm above trough 
   edges) and the Wilhelmy plate is installed skip steps 3 - 6.
3. [Calibrate the Wilhelmy balance](#calibrating-the-wilhelmy-balance)
   if necessary.
4. Hang a clean filter paper Wilhelmy plate from a fine wire on the balance. 
   Make sure that you know the circumference of the plate in mm. This should be 
   recorded in the Jupyter Notebook you are running. Our default 
   circumference is 21.5 mm.
5. The subphase should fill the trough so that it rises 1 - 1.5 mm above the 
   edges of the trough. To add subphase use the clean glass funnel in the trough 
   isolation box to pour through (pouring directly from a bottle splashes). 
   The funnel makes it much easier to add subphase when the polycarbonate lid 
   with just a small opening is in use. Always add subphase between the 
   barriers to trap any surface active species between them for easier removal.
6. Adjust the height of the Wilhelmy balance so the plate is partially 
   submerged in the subphase. The balance settling time is long. You will 
   have to wait at least 1 minute before any measurements will be valid. 
   With a reasonably clean trough and subphase the unzeroed balance should 
   settle to a surface pressure < 10 mN/m. If it does not or shows no noise, 
   there may be a problem.
7. If necessary [initialize the trough](#initialization) then start the 
   trough control and calibration tool by running the command 
   `Trough_GUI.Controls(Trough_GUI.calibrations)` in an empty cell of the 
   notebook.
8. Expand the "Manual Barrier Control" accordian. Set the direction to 
   "open". Set the speed to maximum (~10 cm/min). Click the start button. 
   Watch the surface pressure indicator. When the barriers stop (~12.7 cm 
   separation), wait to make sure the surface pressure has stabilized.
9. Switch the direction to "close". Set the speed to the maximum closing 
   speed (~6.8 cm/min). Click the start button. Watch the surface pressure 
   indicator.
10. Once the barriers are fully closed (~2.8 cm separation), check the 
    surface pressure. If it is greater than it was when fully open carefully 
    aspirate the surface between the barriers without catching the Wilhelmy 
    plate until the surface pressure is slightly less than observed for the 
    open barriers.
11. Repeat steps 8 - 10 up to 4X to get the surface clean. If it is still 
    not clean:
    1. Raise the Wilhelmy balance carefully and rotate it aside. Make 
       sure to lock it in place.
    2. Remove the polycarbonate lid if it is in place. Store it so that it 
       does not get contaminated.
    3. Aspirate all the subphase out of the trough and try again.
12. If after a second try the trough and subphase are still not clean the 
    [trough probably needs to be cleaned](#cleaning-the-trough).
13. When it appears clean test:
    1. Manually open the barriers all the way.
    2. Set up a run by executing the command 
       `Trough_GUI.Collect_Data.Run("XXX")`, where XXX is replaced with a 
       name for the run (e.g. "clean_test_MMM_DD_YYYYa") in an empty cell.
    3. Set the units to cm separation. Set the speed to 1 cm/min. Set the 
       final separation to the minimum for the trough (~2.86 cm).
    4. When the surface pressure is stable click on the "zero pressure" 
       button to tare the Wilhelmy balance.
    5. Click start. The run will stop when the barriers reach the target 
       separation. You can also stop the collection by clicking the "stop" 
       button.
    6. **If the surface pressure stays between -0.2 and +0.2 mN/m the trough 
       is adequately clean.**

## Storage of Trough Between Runs
* If the trough is being used regularly (1X/week or more): store the trough 
  with clean subphase in it. If the subphase is water make sure that the 
  humidification beaker in the isolation box is kept about 50% full.
* If the trough will be unused for a significant time:
  1. [After verifying the trough and subphase cleanliness](#checking-trough-and-subphase-cleanliness)
     aspirate off all the subphase.
  2. Empty the humidification beaker.
  3. Cover the trough with the polycarbonate lid.
  4. Make sure the isolation box is closed.
  5. Make sure the power supply is off.
  6. Shut down the computer.

## Handling Spreading Solvent(s)
**It is extremely easy to contaminate the solvents with surface active 
compounds at a level that will ruin experiments**
* Generally HPLC grade solvents are adequately clean. We most commonly use 
  HPLC grade hexanes and absolute ethanol.
* All glassware must be carefully cleaned before using to transfer or 
  contain spreading solvents.
  1. If unsure of basic cleanliness wash well with soap and water. Rinse 
     five (5) times with warm tap water. Rinse three (3) times with 
     de-ionized water.
  2. Rinse two (2) times with absolute ethanol (10% - 20% container volume per 
     rinse).
  3. Rinse six (6) times with the spreading solvent (10% - 20% container volume 
     per rinse).
* **Do not stick anything into the clean spreading solvent stock bottle.** Get 
  samples to work with by pouring into properly cleaned intermediate containers.

## Checking Spreading Solvent Cleanliness
1. Transfer < 1 mL of spreading solvent to a
   [properly cleaned](#handling-spreading-solvents) vial.
2. [Initialize the trough](#initialization) and 
   [verify that the subphase is clean.](#checking-trough-and-subphase-cleanliness)
3. Using the "Manual Barrier Controls" open the barriers all the way.
4. Rinse the positive displacement microdispenser 3X with absolute ethanol 
   from a TFE squeeze bottle and then 3X with HPLC grade hexanes from a TFE 
   squeeze bottle.
5. Rinse with the solvent sample being tested 6X by sucking up 90 &micro;L 
   of the solvent sample and dispensing it into a waste beaker.
6. Dispense 90 &micro;L of the solvent sample onto the surface between the 
   barriers.
7. Allow to evaporate (15 min is adequate for hexanes).
8. [Perform a compression](#running-a-compression) at 1 cm/min from fully 
   open to fully closed.
9. **The solvent is clean if the surface pressure stays between -0.2 and +0.2 
   mN/m.**

## Making a Spreading Solution
For most molecules we want to spread about 3.00 X 10<sup>-8</sup> moles of 
molecules on our trough to get a range of roughly 60 to 15 square Angstroms per 
molecule during a compression.
1. The ideal volume to spread is 50 &micro;L of solution. Thus we want a 
   concentration near (3.00 X 10<sup>-8</sup> moles)/(50.0 X 10<sup>-6</sup> L)
   = 6 X 10<sup>-4</sup> M. It is practical to spread anywhere between 20 
   and 90 &micro;L. So, you can adapt to concentrations that vary between 1.00 
   x 10<sup>-3</sup> M and 3.3 X 10<sup>-4</sup> M.
2. Ideally your molecule will dissolve in pure hexanes at a concentration of 
   6 X 10<sup>-4</sup> M. If it is not soluble you can put a few percent (up 
   to 5% v/v) of ethanol in with the hexanes. This solvent mixture works for 
   many surfactants, without significantly impacting the surface tension of 
   a water subphase.
3. Experiments take very little solution, so make as small volumes of 
   solution as possible. Note that you should not try to measure out 
   surfactant in amounts that produce less than three significant figures on 
   a standard analytical balance (e.g. at least 10 mg, preferably 50 mg or 
   more.) This may mean that you will have to make a stock solution and 
   dilute it to get in the correct concentration range.
4. All solutions must be made using 
   [properly cleaned glassware](#handling-spreading-solvents) and spreading 
   solvents that have been
   [verified to be clean.](#checking-spreading-solvent-cleanliness) Use 
   volumetric flasks with ground glass stoppers to avoid contamination by 
   the plasticizers found in most polymer caps.
5. Because the solvents are very volatile the solutions will not keep long 
   in the volumetric flasks with ground glass stoppers. They can be 
   transferred for somewhat longer term storage to sealed brown bottles 
   if the bottles are 
   [properly washed](#checking-spreading-solvent-cleanliness) 
   and you have verified that a little solvent stored in the bottle 
   overnight and shaken [stays clean.](#checking-spreading-solvent-cleanliness)

## Spreading a Sample
1. Rinse a small vial 2X with absolute ethanol from a TFE squeeze bottle 
   then 3X with hexanes from a TFE squeeze bottle.
2. If you need to use a pipette or funnel (the funnel is a better choice as 
   you are less likely to contaminate the stock spreading solution) to transfer 
   the spreading solution to the vial rinse the pipette or funnel 2X with 
   absolute ethanol from a TFE squeeze bottle and then 3X with hexanes from 
   a TFE squeeze bottle.
3. Rinse the transfer tool with the spreading solution 6X.
4. Rinse the vial 6X (10-20% of vial volume) with the spreading solution.
5. Use the transfer tool to transfer about 1 mL of the spreading solution to 
   the small vial.
6. Set the positive displacement dispenser to the volume you will be 
   dispensing.
7. Rinse the dispenser 2X with absolute ethanol from a TFE squeeze bottle 
   then 3X with hexanes from a TFE squeeze bottle. Make sure you move the 
   plunger through its dispensing motion while doing this.
8. When the dispenser is dry, rinse 6X with the spreading solution making 
   sure to take up the full amount to be dispensed on each rinse.
9. With the **barriers fully open** dispense the spreading solution drop wise 
   onto the surface between the barriers. Avoid the Wilhelmy plate.
10. Allow time for the solvent to evaporate (~ 15 minutes for hexanes) 
    before doing a compression.

## Running a Compression
1. Trough must first be
   [verified to be clean](#checking-trough-and-subphase-cleanliness).
2. Spread the surfactant solution on the trough with the barriers open. 
   Allow sufficient time for the solvent to evaporate (~15 min for hexanes). 
   The amount to spread will depend on your target range for area per 
   molecule and the concentration of your solution (10<sup>-4</sup> - 
   10<sup>-3</sup> M is typical).
3. In a new notebook cell execute the command 
   `Trough_GUI.Collect_Data.Run("XXX")`, where XXX is replaced with a 
       name for the run (e.g. "CompoundName_MMM_DD_YYYYa")
4. Adjust the moles of molecules to the moles of surfactant you spread. 
   Adjust the units to Angstroms squared per molecule. Choose your desired 
   final target area and compression speed.
5. When the solvent is fully evaporated zero the balance.
6. Store the settings.
7. When ready click the "Start" button. The collection will stop when the 
   desired area is reached. You can also stop the run by clicking the "Stop" 
   button.

## Calibrating the Wilhelmy Balance
**This should be done at the beginning of any day real data is collected**
1. If it is not already running launch the trough control and calibration 
   tool by running the command `Trough_GUI.Controls(Trough_GUI.calibrations)
   ` in an empty notebook cell.
2. Expand the "Calibrate Balance" accordian and follow the on screen 
   instructions.

## Calibrating Barrier Position and Speed
**This only needs to be done if a check of the measured barrier separation 
is off by more than ±0.03 mm**
1. If it is not already running launch the trough control and calibration 
   tool by running the command `Trough_GUI.Controls(Trough_GUI.calibrations)
   ` in an empty notebook cell.
2. Expand the "Calibrate Barriers" accordian and follow the on screen 
   instructions.

## Calibrating the Temperature Probe.
**This is very stable so should not need to be done often**
1. If it is not already running launch the trough control and calibration 
   tool by running the command `Trough_GUI.Controls(Trough_GUI.calibrations)
   ` in an empty notebook cell.
2. Expand the "Calibrate Temperature" accordian and follow the on screen 
   instructions.
3. A good source of known temperatures is the thermostat recirculator.

## Cleaning the Trough
1. The cleaning solution 1:1 concentrated nitric acid:concentrated sulfuric 
   acid is extremely dangerous and also has potential to damage parts of the 
   trough. Do not perform this cleaning procedure until Dr. Guto has 
   certified you for the process.
2. The trough can be powered down during this procedure.
3. The Wilhelmy balance should be locked in position out of the way.
4. The polycarbonate lid should be removed (store it so that does not get 
   contaminated).
5. Fill the trough with the 1:1 concentrated nitric:sulfuric acid solution. 
   Allow to sit 10 + minutes.
6. While the cleaning solution sits in the trough make sure the aspirator 
   trap is dry.
7. Aspirate off the cleaning solution. 
   * Unless the trough is extremely dirty the collected cleaning 
     solution may be returned to the cleaning solution storage bottle.
   * If disposing of the cleaning solution treat it as strong acid waste and 
     neutralize properly.
8. Rinse the trough twice with clean water subphase.
9. [Check the cleanliness of the trough](#checking-trough-and-subphase-cleanliness)