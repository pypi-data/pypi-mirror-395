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


def configure_ue31pp_motor(esp, axis=1):
    """
    Configures ESP301 to use the UE72PP stepper motor
    """
    step = 1/200.
    print(f"=== UE72 Motor Configuration on Axis {axis} ===\n")
    esp.clear_errors()

    # Configuration initiale
    send_checked(esp, f'{axis}MF')
    send_checked(esp, f'{axis}DH')

    # Configuration du microstepping à 100
    send_checked(esp, f'{axis}QM3')
    print(esp.query(f"{axis}QM?").strip())

    # Passer en mode degrés (unité 7)
    send_checked(esp, f'{axis}SN7')
    print(esp.query(f"{axis}SN?").strip())

    # Définir le nombre de pas par unité (degré)
    # 200 steps = 1 degré (sans microstepping)
    send_checked(esp, f'{axis}SU0.01')
    print(esp.query(f"{axis}SU?").strip())

    # Reste de la configuration
    send_checked(esp, f'{axis}QI0.6')
    print(esp.query(f"{axis}QI?").strip())

    send_checked(esp, f'{axis}QV30')
    print(esp.query(f"{axis}QV?").strip())

    send_checked(esp, f'{axis}QS100')
    print(esp.query(f"{axis}QS?").strip())

    send_checked(esp, f'{axis}FR{step*2}')
    print(esp.query(f"{axis}FR?").strip())

    send_checked(esp, f'{axis}QD')

    # Vitesses et accélérations en degrés/s et degrés/s²
    send_checked(esp, f'{axis}VU2')
    print('Max velocity', esp.query(f"{axis}VA?").strip())
    send_checked(esp, f'{axis}VA2')
    print('Velocity', esp.query(f"{axis}VA?").strip())

    send_checked(esp, f'{axis}AU5')
    send_checked(esp, f'{axis}AC5')
    print(esp.query(f"{axis}AC?").strip())

    send_checked(esp, f'{axis}AG5')
    print(esp.query(f"{axis}AG?").strip())

    send_checked(esp, f'{axis}QR1000,30')

    print("\nConfiguring software limits...")
    send_checked(esp, f"{axis}SR10000")  # + limit at 10000mm (instead of 1000)
    send_checked(esp, f"{axis}SL-10000")  # - limit at -10000mm (instead of -1000)
    print(f"   Limits: -10000 to +10000 mm")

    print("\nDisabling hardware limits...")
    send_checked(esp, f'{axis}ZH0')  # Disable hardware limits
    print(f"   Status:", print(esp.query(f'{axis}ZH?').strip()))

    # Activation du moteur
    print("\nActivating motor...")
    send_checked(esp, f"{axis}MO")

    # SAVE
    print("\nSaving...")
    if not send_checked(esp, "SM"):
        print("   (SM not supported, temporary config)")


    print("\n=== Configuration complete ===")

    esp.clear_errors()



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
    print(f"+ Limit (SR): {sr} deg")
    print(f"- Limit (SL): {sl} deg")

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

    print(f"✓ Limits OK: movement range = {sr_val - sl_val:.1f} deg")
    return True


def diagnose_stop(esp, axis=2, value=0.1):
    """
    Tests if a movement completes correctly
    """
    print("\n=== STOP CONDITION DIAGNOSTIC ===\n")

    # Reset position
    esp.send_command(f"{axis}DH")

    import time

    print(f"Requesting a movement of {value}deg...")
    print("We'll monitor in real-time what happens\n")

    pos_before = float(esp.query(f"{axis}TP?").strip())
    print(f"Position before: {pos_before} deg")

    # Start movement
    esp.send_command(f"{axis}PR{value}")

    # Monitor for 10 seconds (increased from 5 to 10)
    for i in range(100):  # 10 seconds
        time.sleep(0.1)
        try:
            pos = float(esp.query(f"{axis}TP?").strip())
            md = esp.query(f"{axis}MD?").strip()

            print(f"t={i * 0.1:.1f}s | Position: {pos:.4f} deg | MD (done?): {md}", end='\r')

            if md == '1':
                print(f"\n✓ Movement complete at t={i * 0.1:.1f}s")
                print(f"  Final position: {pos} deg")
                print(f"  Displacement: {pos - pos_before} deg")

                # Check overshoot
                overshoot = abs((pos - pos_before) - value)
                if overshoot > 0.01:
                    print(f"  ⚠️ Overshoot detected: {overshoot:.3f} deg")

                return True
        except Exception as e:
            print(f"\n✗ Error: {e}")
            break

    print(f"\n✗ TIMEOUT after 10s")
    pos_final = float(esp.query(f"{axis}TP?").strip())
    print(f"  Position when stopped: {pos_final} deg")
    print(f"  Displacement: {pos_final - pos_before} deg")

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
    print(f"  Resolution (FR): {esp.query(f'{axis}FR?').strip()} deg/step")

    print("\nMOTION:")
    print(f"  Velocity (VA): {esp.query(f'{axis}VA?').strip()} deg/s")
    print(f"  Acceleration (AC): {esp.query(f'{axis}AC?').strip()} deg/s²")
    print(f"  Deceleration (AG): {esp.query(f'{axis}AG?').strip()} deg/s²")

    print("\nLIMITS:")
    print(f"  + Limit (SR): {esp.query(f'{axis}SR?').strip()} deg")
    print(f"  - Limit (SL): {esp.query(f'{axis}SL?').strip()} deg")

    print("\nSTATE:")
    print(f"  Position (TP): {esp.query(f'{axis}TP?').strip()} deg")
    print(f"  Motion done (MD): {esp.query(f'{axis}MD?').strip()}")

    # Additional parameters
    print("\nADVANCED PARAMETERS:")
    try:
        deg = esp.query(f'{axis}MM?').strip()
        print(f"  Control mode (MM): {deg} (0=open-loop)")
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
        print(f"   Software + limit: {sr} deg")
        print(f"   Software - limit: {sl} deg")
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
    print(f"\nInitial position: {pos_init}deg")

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
                print(f"  ✓ Complete → Total position: {pos}deg")
                break
        else:
            print(f"  ✗ Timeout!")
            break

    pos_final = float(esp.query(f"{axis}TP?").strip())
    print(f"\n{'='*60}")
    print(f"Final position: {pos_final}deg")
    print(f"Total displacement: {pos_final - pos_init}deg")
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
        print(f"  {val:5.2f} deg : {status}")

    # Find the limit
    failures = [val for val, success in results if not success]
    if failures:
        print(f"\n⚠️  Motor fails starting from {min(failures)} deg")
    else:
        print(f"\n✓ All tests successful up to {max(val for val, _ in results)} deg")


if __name__ == "__main__":
    from pycarmat.ressources.ESP import ESP30xController
    axis = 2

    with ESP30xController(serial_port='ASRL/dev/ttyUSB0', raise_error=False) as esp:
        # 1. Reset controller
        reset_controller(esp, wait=8)

        # 2. Configuration with fixes
        configure_ue31pp_motor(esp, axis=axis)
        # exit(0)

        # 3. Check limits
        if not check_limits(esp, axis=axis):
            print("\n❌ Stop: incorrect limits")
            exit(1)

        # 4. Display complete configuration
        # display_complete_configuration(esp, axis=axis)

        # 4b. Diagnose hardware limits
        # diagnose_hardware_limits(esp, axis=axis)
        sleep(3)
        send_checked(esp, '2PR1')
        sleep(3)

        # 5. Series movements test
        run_series_movements(esp, axis=axis)

        # 6. Successive movements test (workaround)
        # run_successive_movements(esp, axis=axis)