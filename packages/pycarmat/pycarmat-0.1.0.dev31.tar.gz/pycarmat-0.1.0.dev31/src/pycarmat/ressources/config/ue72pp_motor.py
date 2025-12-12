"""
UE72 Stepper Motor Configuration for ESP301
FIXES FOR THE 2MM STOP PROBLEM

UE72 Motor:
- Type: Permanent magnet
- Nominal voltage: 5.3V
- Nominal current: 1.6A
- Resistance/winding: 3.3Ω
- Inductance/winding: 9mH
- Step: 200 steps/revolution (1.8° per step)
"""
from time import sleep


def send_checked(esp, cmd: str):
    """
    Sends a command to ESP301 and checks the error buffer.
    Returns True if no error detected, otherwise False.
    """
    esp.send_command(cmd)
    err = esp.query("TB?").strip()
    # Format: "code, timestamp, message"
    # Code 0 = NO ERROR
    err_code = err.split(',')[0].strip()
    if err_code != '0':
        print(f"⚠️  Error after '{cmd}': {err}")
        return False
    return True


def configure_ue72pp_motor(esp, axis=2, screw_pitch_mm=0.01):
    """
    Configures ESP301 to use the UE72PP stepper motor
    """
    print(f"=== UE72 Motor Configuration on Axis {axis} ===\n")

    # Calculate resolution in mm
    mm_per_rot = 1/200

    # 1. DEFINE MOTOR TYPE
    print("1. Defining motor type...")
    send_checked(esp, f"{axis}QM3")
    response = esp.query(f"{axis}QM?")
    print(f"   Motor type: {response.strip()}")
    print("1b. Updating driver...")
    send_checked(esp, f"{axis}QD")

    # 2. DEFINE MAXIMUM CURRENT
    print("\n2. Configuring maximum current...")
    # 1.6A nominal
    send_checked(esp, f"{axis}QI1.6")
    response = esp.query(f"{axis}QI?")
    print(f"   Maximum current: {response.strip()} A")

    # 3. DEFINE MICROSTEP FACTOR
    print("\n3. Configuring microstep factor...")
    microstep = 10
    send_checked(esp, f"{axis}QS{microstep}")
    response = esp.query(f"{axis}QS?")
    print(f"   Microstep factor: {response.strip()}")

    # 4. DEFINE FULL STEP RESOLUTION
    print("\n4a. Configuring step unit...")
    send_checked(esp, f"{axis}SU{screw_pitch_mm}")
    response = esp.query(f"{axis}SU?")
    print(f"   Step unit: {response.strip()} step/mm")

    print("\n4b. Configuring resolution...")
    # FINAL FIX: 2x overshoot observed experimentally
    # Motor always makes 2x more movement than requested
    # Solution: Multiply FR by 2
    full_step_resolution = mm_per_rot * 2
    send_checked(esp, f"{axis}FR{full_step_resolution}")
    response = esp.query(f"{axis}FR?")
    print(f"   Resolution: {response.strip()} mm/step")
    print(f"   ⚠️ FIX: FR multiplied by 2 to correct x2 overshoot")

    full_step_resolution = mm_per_rot * 2
    send_checked(esp, f"{axis}SU{full_step_resolution}")
    response = esp.query(f"{axis}FR?")
    print(f"   Resolution: {response.strip()} mm/step")
    send_checked(esp, f"{axis}SU0.01")

    # 5. UPDATE DRIVER
    print("\n5. Updating driver...")
    send_checked(esp, f"{axis}QD")

    # 6. DEFINE UNITS
    print("\n6. Configuring units...")
    send_checked(esp, f"{axis}SN2")  # 2 = millimeter
    print(f"   Units: millimeters")

    # 6b. CONFIGURE SOFTWARE LIMITS (INCREASED)
    print("\n6b. Configuring software limits...")
    send_checked(esp, f"{axis}SR10000")  # + limit at 10000mm (instead of 1000)
    send_checked(esp, f"{axis}SL-10000")  # - limit at -10000mm (instead of -1000)
    print(f"   Limits: -10000 to +10000 mm")

    # 6c. CHECK AND CONFIGURE BUFFER (NEW)
    print("\n6c. Configuring buffer...")
    try:
        bp = esp.query(f"{axis}BP?").strip()
        print(f"   Current Buffer Pointer (BP): {bp}")
    except:
        print(f"   Buffer Pointer (BP): command unavailable")

    # Increase buffer if possible
    send_checked(esp, f"{axis}BP10000")
    print(f"   Buffer extended to 10000")

    # 7. DEFINE MAX LIMITS
    print("\n7. Configuring maximum limits...")
    send_checked(esp, f"{axis}VU5")  # Max velocity: 5 mm/s
    print(f"   Max velocity (VU): 5 mm/s")

    send_checked(esp, f"{axis}AU100")  # Max acceleration: 100 mm/s²
    print(f"   Max acceleration (AU): 100 mm/s²")

    # 8. CONFIGURE TRAJECTORY PARAMETERS (MODIFIED)
    print("\n8. Configuring motion parameters...")

    # TIMEOUT FIX: Increase speed to avoid timeouts
    send_checked(esp, f"{axis}VA0.5")  # 0.5 instead of 0.1 mm/s
    print(f"   Velocity: 0.5 mm/s (increased to avoid timeout)")

    # Keep moderate acceleration
    send_checked(esp, f"{axis}AC1")  # 1 instead of 0.5 mm/s²
    print(f"   Acceleration: 1 mm/s²")

    # Keep high deceleration
    send_checked(esp, f"{axis}AG5")
    print(f"   Deceleration: 5 mm/s² (high for precise stop)")

    # 9. TORQUE REDUCTION
    print("\n9. Configuring torque reduction...")
    send_checked(esp, f"{axis}QR1000,30")
    print(f"   Reduction: 30% after 1s")

    # 11. SAVE
    print("\n11. Saving...")
    if not send_checked(esp, "SM"):
        print("   (SM not supported, temporary config)")

    # 12. ENABLE AXIS
    print("\n12. Activating motor...")
    send_checked(esp, f"{axis}MO")

    print("\n=== Configuration complete ===")
    print(f"Effective resolution: {full_step_resolution / microstep:.6f} mm/micro-step")


def reset_controller(esp, wait: float):
    """
    Complete reset of ESP301 controller
    """
    print("\n⚠️  CONTROLLER RESET IN PROGRESS...")
    print("   The controller will restart (may take up to 20s)")
    esp.send_command("RS")
    print("   Reset sent. Wait for controller to restart.")
    sleep(wait)


def check_limits(esp, axis=2):
    """Checks that limits allow movement"""
    print("\n=== Checking Limits ===")
    sr = esp.query(f"{axis}SR?").strip()
    sl = esp.query(f"{axis}SL?").strip()
    print(f"+ Limit (SR): {sr} mm")
    print(f"- Limit (SL): {sl} mm")

    sr_val = float(sr)
    sl_val = float(sl)

    if sr_val <= 0.01:
        print("⚠️  PROBLEM: + limit is at zero or negative!")
        print("   Motor cannot move forward!")
        return False

    if sl_val >= -0.01:
        print("⚠️  PROBLEM: - limit is at zero or positive!")
        print("   Motor cannot move backward!")
        return False

    print(f"✓ Limits OK: movement range = {sr_val - sl_val:.1f} mm")
    return True


def diagnose_stop(esp, axis=2, value=0.1):
    """
    Tests if a movement completes correctly
    """
    print("\n=== STOP CONDITION DIAGNOSTIC ===\n")

    # Reset position
    esp.send_command(f"{axis}DH")

    import time

    print(f"Requesting a movement of {value}mm...")
    print("We'll monitor in real-time what happens\n")

    pos_before = float(esp.query(f"{axis}TP?").strip())
    print(f"Position before: {pos_before} mm")

    # Start movement
    esp.send_command(f"{axis}PR{value}")

    # Monitor for 10 seconds (increased from 5 to 10)
    for i in range(100):  # 10 seconds
        time.sleep(0.1)
        try:
            pos = float(esp.query(f"{axis}TP?").strip())
            md = esp.query(f"{axis}MD?").strip()

            print(f"t={i * 0.1:.1f}s | Position: {pos:.4f} mm | MD (done?): {md}", end='\r')

            if md == '1':
                print(f"\n✓ Movement complete at t={i * 0.1:.1f}s")
                print(f"  Final position: {pos} mm")
                print(f"  Displacement: {pos - pos_before} mm")

                # Check overshoot
                overshoot = abs((pos - pos_before) - value)
                if overshoot > 0.01:
                    print(f"  ⚠️ Overshoot detected: {overshoot:.3f} mm")

                return True
        except Exception as e:
            print(f"\n✗ Error: {e}")
            break

    print(f"\n✗ TIMEOUT after 10s")
    pos_final = float(esp.query(f"{axis}TP?").strip())
    print(f"  Position when stopped: {pos_final} mm")
    print(f"  Displacement: {pos_final - pos_before} mm")

    # Force stop
    esp.send_command(f"{axis}ST")
    return False


def display_complete_configuration(esp, axis=2):
    """Displays current configuration"""
    print(f"\n=== Axis {axis} Configuration ===\n")

    print("MOTOR:")
    print(f"  Type (QM): {esp.query(f'{axis}QM?').strip()}")
    print(f"  Current (QI): {esp.query(f'{axis}QI?').strip()} A")
    print(f"  Microstep (QS): {esp.query(f'{axis}QS?').strip()}")
    print(f"  Resolution (FR): {esp.query(f'{axis}FR?').strip()} mm/step")

    print("\nMOTION:")
    print(f"  Velocity (VA): {esp.query(f'{axis}VA?').strip()} mm/s")
    print(f"  Acceleration (AC): {esp.query(f'{axis}AC?').strip()} mm/s²")
    print(f"  Deceleration (AG): {esp.query(f'{axis}AG?').strip()} mm/s²")

    print("\nLIMITS:")
    print(f"  + Limit (SR): {esp.query(f'{axis}SR?').strip()} mm")
    print(f"  - Limit (SL): {esp.query(f'{axis}SL?').strip()} mm")

    print("\nSTATE:")
    print(f"  Position (TP): {esp.query(f'{axis}TP?').strip()} mm")
    print(f"  Motion done (MD): {esp.query(f'{axis}MD?').strip()}")

    # Additional parameters
    print("\nADVANCED PARAMETERS:")
    try:
        mm = esp.query(f'{axis}MM?').strip()
        print(f"  Control mode (MM): {mm} (0=open-loop)")
    except:
        print(f"  Control mode (MM): Not available")

    try:
        hc = esp.query(f'{axis}HC?').strip()
        print(f"  Holding Current (HC): {hc} A")
    except:
        print(f"  Holding Current (HC): Not available")

    try:
        bp = esp.query(f'{axis}BP?').strip()
        print(f"  Buffer Pointer (BP): {bp}")
    except:
        print(f"  Buffer Pointer (BP): Not available")


def diagnose_hardware_limits(esp, axis=2):
    """
    Checks if hardware limits are blocking movement
    """
    print("\n" + "="*60)
    print("HARDWARE LIMITS DIAGNOSTIC")
    print("="*60)

    # Check limit switch state
    print("\n1. Hardware limit state:")
    try:
        # Check if limits are enabled
        lh = esp.query(f"{axis}LH?").strip()
        print(f"   Hardware limits (LH): {lh}")
    except:
        print(f"   Hardware limits (LH): Not available")

    # Check current state
    print("\n2. Current motor state:")
    try:
        ts = esp.query(f"{axis}TS?").strip()
        print(f"   Motor status (TS): {ts}")
        # Decode status (bits)
        status = int(ts.split(',')[0]) if ',' in ts else int(ts)
        print(f"   Bit 0 (Error): {bool(status & 1)}")
        print(f"   Bit 1 (In Motion): {bool(status & 2)}")
        print(f"   Bit 2 (+Limit): {bool(status & 4)}")
        print(f"   Bit 3 (-Limit): {bool(status & 8)}")
    except Exception as e:
        print(f"   Motor status (TS): Not available ({e})")

    # Check errors
    print("\n3. Recent errors:")
    err = esp.query("TB?").strip()
    print(f"   Error buffer: {err}")

    # Check limit parameters
    print("\n4. Limit parameters:")
    try:
        # Software limits
        sr = esp.query(f"{axis}SR?").strip()
        sl = esp.query(f"{axis}SL?").strip()
        print(f"   Software + limit: {sr} mm")
        print(f"   Software - limit: {sl} mm")
    except:
        pass

    print("\n" + "="*60)


def run_successive_movements(esp, axis=2):
    """
    Tests if 5mm can be reached by making several small movements
    """
    print("\n" + "="*60)
    print("SUCCESSIVE MOVEMENTS TEST (workaround)")
    print("Goal: Reach 5mm by making 5× 1mm")
    print("="*60)

    import time

    # Reset position
    esp.send_command(f"{axis}DH")
    time.sleep(0.5)

    pos_init = float(esp.query(f"{axis}TP?").strip())
    print(f"\nInitial position: {pos_init}mm")

    # Make 5 movements of 1mm
    for i in range(5):
        print(f"\n--- Movement {i+1}/5: +1mm ---")

        esp.send_command(f"{axis}PR1")

        # Wait for movement to finish
        for j in range(150):  # 15 seconds max
            time.sleep(0.1)
            md = esp.query(f"{axis}MD?").strip()

            if md == '1':
                pos = float(esp.query(f"{axis}TP?").strip())
                print(f"  ✓ Complete → Total position: {pos}mm")
                break
        else:
            print(f"  ✗ Timeout!")
            break

    pos_final = float(esp.query(f"{axis}TP?").strip())
    print(f"\n{'='*60}")
    print(f"Final position: {pos_final}mm")
    print(f"Total displacement: {pos_final - pos_init}mm")
    print(f"Goal: 5mm → {'✓ SUCCESS' if abs(pos_final - pos_init - 5) < 0.1 else '✗ FAILURE'}")
    print(f"{'='*60}")


def run_series_movements(esp, axis=2):
    """
    Tests a series of movements of different distances
    """
    print("\n" + "="*60)
    print("MOVEMENT SERIES TEST")

    test_values = [0.1, 0.2, 0.5, 0.75, 1.0, 2.0, 3.0, 5.0]
    results = []

    for val in test_values:
        success = diagnose_stop(esp, axis=axis, value=val)
        results.append((val, success))

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for val, success in results:
        status = "✓ OK" if success else "✗ FAILURE"
        print(f"  {val:5.2f} mm : {status}")

    # Find the limit
    failures = [val for val, success in results if not success]
    if failures:
        print(f"\n⚠️  Motor fails starting from {min(failures)} mm")
    else:
        print(f"\n✓ All tests successful up to {max(val for val, _ in results)} mm")


if __name__ == "__main__":
    from pycarmat.ressources.ESP import ESP30xController
    axis = 1

    with ESP30xController(serial_port='ASRL/dev/ttyUSB0', raise_error=False) as esp:
        # 1. Reset controller
        reset_controller(esp, wait=8)

        # 2. Configuration with fixes
        configure_ue72pp_motor(esp, axis=axis, screw_pitch_mm=0.01)
        # exit(0)

        # 3. Check limits
        if not check_limits(esp, axis=axis):
            print("\n❌ Stop: incorrect limits")
            exit(1)

        # 4. Display complete configuration
        display_complete_configuration(esp, axis=axis)

        # 4b. Diagnose hardware limits
        diagnose_hardware_limits(esp, axis=axis)

        # 5. Series movements test
        run_series_movements(esp, axis=axis)

        # 6. Successive movements test (workaround)
        run_successive_movements(esp, axis=axis)