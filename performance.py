import subprocess
import time

def measure_run_time(filename, method, num_trials=5):
    """
    Measure the execution time of the inference engine script multiple times.
    
    Args:
        filename (str): The knowledge base file to process.
        method (str): The inference method (TT, FC, or BC).
        num_trials (int): Number of times to run the script for averaging.
        
    Returns:
        float: Average execution time.
    """
    times = []
    
    for _ in range(num_trials):
        start_time = time.time()
        
        result = subprocess.run(
            ["python", "main.py", filename, method],
            capture_output=True,
            text=True
        )
        
        end_time = time.time()
        
        if result.returncode != 0:
            print(f"Error in running main.py: {result.stderr}")
            return None
        
        times.append(end_time - start_time)
    
    
    average_time = sum(times) / len(times)
    
    return average_time

if __name__ == "__main__":
    filename = "testcase/TT-WK1.txt"  
    method = "TT"  
    
    print(f"Measuring the performance of {method} on {filename}...")

    avg_time = measure_run_time(filename, method)
    
    if avg_time is not None:
        print(f"Average execution time over 5 trials: {avg_time:.4f} seconds")
