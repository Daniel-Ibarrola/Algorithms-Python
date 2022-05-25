import heapq


class Job:

    def __init__(self, thread: int, finish_time: int):
        self.thread = thread
        self.finish_time = finish_time

    def __eq__(self, other: "Job") -> bool:
        return self.finish_time == other.finish_time

    def __lt__(self, other: "Job") -> bool:
        if self.finish_time == other.finish_time:
            return self.thread < other.thread
        return self.finish_time < other.finish_time

    def __repr__(self):
        return f"Job(Thread={self.thread}, Finish={self.finish_time})"


def assign_jobs(num_threads: int, jobs: list[int]) -> tuple[list, list]:
    """ Assigns each job to a worker """
    assigned_workers = []
    start_times = []
    free_times = []
    for ii in range(num_threads):
        free_times.append(Job(ii, 0))

    for ii in range(len(jobs)):
        current_job = heapq.heappop(free_times)
        assigned_workers.append(current_job.thread)
        start_times.append(current_job.finish_time)
        heapq.heappush(free_times, Job(current_job.thread, current_job.finish_time + jobs[ii]))

    assert len(assigned_workers) == len(start_times)
    return assigned_workers, start_times


def print_jobs(workers: list[int], start_times: list[int]) -> None:
    for ii in range(len(workers)):
        print(workers[ii], start_times[ii])


def main():
    print(f"\nJob queue 1")
    jobs = [1, 2, 3, 4, 5]
    workers, start_times = assign_jobs(2, jobs)
    print_jobs(workers, start_times)

    print(f"\nJob queue 2")
    jobs = [1] * 20
    workers, start_times = assign_jobs(4, jobs)
    print_jobs(workers, start_times)


if __name__ == "__main__":
    main()
