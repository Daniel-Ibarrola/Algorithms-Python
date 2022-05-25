import heapq


class JobQueue:

    def __init__(self, num_workers: int, jobs: list[int]):
        self.num_workers = num_workers  # Number of threads
        self.jobs = jobs
        self.assigned_workers = []
        self.start_times = []

    def read_data(self) -> None:
        """ Reads the following data from user input: number of workers or threads, list with jobs
            processing times
        """
        self.num_workers, m = map(int, input().split())
        self.jobs = list(map(int, input().split()))
        assert m == len(self.jobs), f"m={m}, len={len(self.jobs)}"

    def write_response(self) -> None:
        """ Prints in each line the thread or worker that will process
            the i-th job and the time when it will start processing it.
        """
        for ii in range(len(self.jobs)):
            print(self.assigned_workers[ii], self.start_times[ii])

    def assign_jobs(self) -> None:
        """ Assigns each job to a worker using a naive and slow algorithm."""
        self.assigned_workers = [None] * len(self.jobs)
        self.start_times = [None] * len(self.jobs)
        next_free_time = [0] * self.num_workers
        for i in range(len(self.jobs)):
            next_worker = 0
            for j in range(self.num_workers):
                if next_free_time[j] < next_free_time[next_worker]:
                    next_worker = j
            self.assigned_workers[i] = next_worker
            self.start_times[i] = next_free_time[next_worker]
            next_free_time[next_worker] += self.jobs[i]

    def solve(self, read_data=False) -> None:
        """ Assigns the jobs and prints the results.
        """
        if read_data:
            self.read_data()
        self.assign_jobs()
        self.write_response()


def main():

    print(f"Job queue 1")
    job_queue = JobQueue(2, [1, 2, 3, 4, 5])
    job_queue.solve()

    print(f"\nJob queue 2")
    jobs = [1] * 20
    job_queue = JobQueue(4, jobs)
    job_queue.solve()


if __name__ == '__main__':
    main()

