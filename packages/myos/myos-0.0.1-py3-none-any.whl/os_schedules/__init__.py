def _print_code(code_str):
    print(code_str)

def p1():
    """basic_linux"""
    _print_code(r"""#!/bin/bash
# Practical 1: Basic Linux Commands
echo "--- PRACTICAL 1: Linux Commands ---"
echo "--- executing who ---"
who
echo "--- executing date---"
date
echo "--- executing echo ---"
read -p "Enter a string to echo (Demo: Hello OS): " user_string
echo "You entered: $user_string"
""")

basic_linux = p1
def p2_1():
    """factorial"""
    _print_code(r"""#!/bin/bash
# Practical 2.1: Factorial
echo "--- PRACTICAL 2.1: Factorial ---"
read -p "Enter a number (Demo: Try 5): " num
fact=1
for ((i=2;i<=num;i++)); do fact=$((fact * i)); done
echo "Factorial of $num is $fact"
""")

factorial = p2_1
def p2_2():
    """greatest_of_3"""
    _print_code(r"""#!/bin/bash
# Practical 2.2: Greatest of 3
echo "--- PRACTICAL 2.2: Greatest of 3 ---"
read -p "Enter 3 nums (Demo: 10 25 15): " n1 n2 n3
if [ $n1 -gt $n2 ] && [ $n1 -gt $n3 ]; then echo "$n1 is max";
elif [ $n2 -gt $n1 ] && [ $n2 -gt $n3 ]; then echo "$n2 is max";
else echo "$n3 is max"; fi
""")

greatest_of_3 = p2_2
def p2_3():
    """reverse_num"""
    _print_code(r"""#!/bin/bash
# Practical 2.3: Reverse Number
echo "--- PRACTICAL 2.3: Reverse Number ---"
read -p "Enter num (Demo: 1234): " n
rev=0
while [ $n -gt 0 ]; do rem=$((n%10)); rev=$((rev*10+rem)); n=$((n/10)); done
echo "Reverse: $rev"
""")

reverse_num = p2_3
def p2_4():
    """even_odd"""
    _print_code(r"""#!/bin/bash
# Practical 2.4: Array Even Odd
echo "--- PRACTICAL 2.4: Even/Odd Array ---"
read -p "Enter nums separated by space (Demo: 1 2 3 4 5): " -a arr
for i in "${arr[@]}"; do if [ $((i%2)) -eq 0 ]; then echo "$i Even"; else echo "$i Odd"; fi; done
""")

even_odd = p2_4
def p3():
    """mult_table"""
    _print_code(r"""#!/bin/bash
# Practical 3: Table
echo "--- PRACTICAL 3: Multiplication Table ---"
read -p "Enter Number (Demo: 5): " n
for ((i=1;i<=10;i++)); do echo "$n * $i = $((n*i))"; done
""")

mult_table = p3
def p6():
    """fork_demo"""
    _print_code(r"""#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
// Practical 6: Fork System Call
int main() {
    printf("--- PRACTICAL 6: Fork Demo ---\n");
    printf("Forking process now...\n");
    pid_t pid = fork();
    if(pid < 0) printf("Fork failed\n");
    else if(pid == 0) printf("Child (PID %d), Parent (PID %d)\n", getpid(), getppid());
    else { sleep(1); printf("Parent (PID %d), Child (PID %d)\n", getpid(), pid); }
    return 0;
}""")

fork_demo = p6
def p4_1_1():
    """fcfs_interactive"""
    _print_code(r"""#include<stdio.h>
// Practical 4.1.1: FCFS (Interactive)
int main() {
    int n, bt[20], wt[20], tat[20], i, j;
    float avwt=0, avtat=0;
    printf("--- FCFS Interactive ---\n");
    printf("Tip: Try 3 processes with Burst Times: 10, 5, 8\n");
    printf("Enter total processes: "); scanf("%d", &n);
    for(i=0;i<n;i++) { printf("P%d Burst Time: ",i+1); scanf("%d",&bt[i]); }
    wt[0]=0;
    for(i=1;i<n;i++) { wt[i]=0; for(j=0;j<i;j++) wt[i]+=bt[j]; }
    printf("\nP\tBT\tWT\tTAT");
    for(i=0;i<n;i++) {
        tat[i]=bt[i]+wt[i]; avwt+=wt[i]; avtat+=tat[i];
        printf("\nP%d\t%d\t%d\t%d",i+1,bt[i],wt[i],tat[i]);
    }
    printf("\nAvg WT: %.2f\nAvg TAT: %.2f\n",avwt/n,avtat/n);
    return 0;
}""")

fcfs_interactive = p4_1_1
def p4_1_2():
    """fcfs_static"""
    _print_code(r"""#include <stdio.h>
// Practical 4.1.2: FCFS (Static Hardcoded)
int main() {
    int n = 5, i;
    int AT[] = {0, 1, 2, 3, 4}; 
    int BT[] = {4, 3, 1, 2, 5};
    int CT[5], TAT[5], WT[5], current_time = 0;
    float total_TAT = 0, total_WT = 0;
    printf("--- FCFS Static Mode (No Input Required) ---\n");
    printf("P\tAT\tBT\tCT\tTAT\tWT\n");
    for(i=0; i<n; i++) {
        if(current_time < AT[i]) current_time = AT[i];
        current_time += BT[i];
        CT[i] = current_time;
        TAT[i] = CT[i] - AT[i];
        WT[i] = TAT[i] - BT[i];
        total_TAT += TAT[i]; total_WT += WT[i];
        printf("P%d\t%d\t%d\t%d\t%d\t%d\n", i+1, AT[i], BT[i], CT[i], TAT[i], WT[i]);
    }
    printf("\nAvg TAT = %.2f\nAvg WT  = %.2f\n", total_TAT/n, total_WT/n);
    return 0;
}""")

fcfs_static = p4_1_2
def p4_2_1():
    """sjf_interactive"""
    _print_code(r"""#include<stdio.h>
// Practical 4.2.1: SJF (Interactive)
int main() {
    int n, bt[20], p[20], wt[20], tat[20], i, j, temp;
    float avwt=0, avtat=0;
    printf("--- SJF Interactive ---\n");
    printf("Tip: Try 3 processes with BT: 10, 5, 8\n");
    printf("Processes: "); scanf("%d", &n);
    for(i=0;i<n;i++) { printf("P%d BT: ",i+1); scanf("%d",&bt[i]); p[i]=i+1; }
    for(i=0;i<n;i++) for(j=0;j<n-i-1;j++) if(bt[j]>bt[j+1]) {
        temp=bt[j]; bt[j]=bt[j+1]; bt[j+1]=temp;
        temp=p[j]; p[j]=p[j+1]; p[j+1]=temp;
    }
    wt[0]=0; for(i=1;i<n;i++) { wt[i]=0; for(j=0;j<i;j++) wt[i]+=bt[j]; }
    printf("\nP\tBT\tWT\tTAT");
    for(i=0;i<n;i++) {
        tat[i]=bt[i]+wt[i]; avwt+=wt[i]; avtat+=tat[i];
        printf("\nP%d\t%d\t%d\t%d",p[i],bt[i],wt[i],tat[i]);
    }
    printf("\nAvg WT: %.2f\nAvg TAT: %.2f\n",avwt/n,avtat/n);
    return 0;
}""")

sjf_interactive = p4_2_1
def p4_2_2():
    """sjf_static"""
    _print_code(r"""#include <stdio.h>
// Practical 4.2.2: SJF (Static Hardcoded)
int main() {
    int n=5, i, j, temp, pid[]={1,2,3,4,5}, BT[]={6,2,8,3,4}, CT[5], TAT[5], WT[5], current_time=0;
    float total_TAT=0, total_WT=0;
    for(i=0;i<n;i++) for(j=0;j<n-i-1;j++) if(BT[j]>BT[j+1]) {
        temp=BT[j]; BT[j]=BT[j+1]; BT[j+1]=temp;
        temp=pid[j]; pid[j]=pid[j+1]; pid[j+1]=temp;
    }
    printf("--- SJF Static Mode (No Input Required) ---\n");
    printf("P\tBT\tCT\tTAT\tWT\n");
    for(i=0; i<n; i++) {
        current_time+=BT[i]; CT[i]=current_time;
        TAT[i]=CT[i]; WT[i]=TAT[i]-BT[i];
        total_TAT+=TAT[i]; total_WT+=WT[i];
        printf("P%d\t%d\t%d\t%d\t%d\n", pid[i], BT[i], CT[i], TAT[i], WT[i]);
    }
    printf("\nAvg TAT = %.2f\nAvg WT  = %.2f\n", total_TAT/n, total_WT/n);
    return 0;
}""")

sjf_static = p4_2_2
def p4_3_1():
    """priority_interactive"""
    _print_code(r"""#include<stdio.h>
// Practical 4.3.1: Priority (Interactive)
int main() {
    int n, bt[20], pr[20], p[20], wt[20], tat[20], i, j, temp;
    float avwt=0, avtat=0;
    printf("--- Priority Scheduling Interactive ---\n");
    printf("Tip: Try 3 procs: (BT 10, P 2), (BT 5, P 1), (BT 8, P 3)\n");
    printf("Processes: "); scanf("%d",&n);
    for(i=0;i<n;i++) { printf("P%d BT Priority: ",i+1); scanf("%d %d",&bt[i],&pr[i]); p[i]=i+1; }
    for(i=0;i<n;i++) for(j=0;j<n-i-1;j++) if(pr[j]>pr[j+1]) {
        temp=pr[j]; pr[j]=pr[j+1]; pr[j+1]=temp;
        temp=bt[j]; bt[j]=bt[j+1]; bt[j+1]=temp;
        temp=p[j]; p[j]=p[j+1]; p[j+1]=temp;
    }
    wt[0]=0; for(i=1;i<n;i++) { wt[i]=0; for(j=0;j<i;j++) wt[i]+=bt[j]; }
    printf("\nP\tPri\tBT\tWT\tTAT");
    for(i=0;i<n;i++) {
        tat[i]=bt[i]+wt[i]; avwt+=wt[i]; avtat+=tat[i];
        printf("\nP%d\t%d\t%d\t%d\t%d",p[i],pr[i],bt[i],wt[i],tat[i]);
    }
    printf("\nAvg WT: %.2f\nAvg TAT: %.2f\n",avwt/n,avtat/n);
    return 0;
}""")

priority_interactive = p4_3_1
def p4_3_2():
    """priority_static"""
    _print_code(r"""#include <stdio.h>
// Practical 4.3.2: Priority (Static Hardcoded)
int main() {
    int n=4, i, j, temp, pid[]={1,2,3,4}, BT[]={10,5,8,2}, PR[]={2,0,1,3}, CT[4], TAT[4], WT[4], current_time=0;
    float total_TAT=0, total_WT=0;
    for(i=0;i<n;i++) for(j=0;j<n-i-1;j++) if(PR[j]>PR[j+1]) {
        temp=PR[j]; PR[j]=PR[j+1]; PR[j+1]=temp;
        temp=BT[j]; BT[j]=BT[j+1]; BT[j+1]=temp;
        temp=pid[j]; pid[j]=pid[j+1]; pid[j+1]=temp;
    }
    printf("--- Priority Static Mode (No Input Required) ---\n");
    printf("P\tPri\tBT\tCT\tTAT\tWT\n");
    for(i=0; i<n; i++) {
        current_time+=BT[i]; CT[i]=current_time;
        TAT[i]=CT[i]; WT[i]=TAT[i]-BT[i];
        total_TAT+=TAT[i]; total_WT+=WT[i];
        printf("P%d\t%d\t%d\t%d\t%d\t%d\n", pid[i], PR[i], BT[i], CT[i], TAT[i], WT[i]);
    }
    printf("\nAvg TAT = %.2f\nAvg WT  = %.2f\n", total_TAT/n, total_WT/n);
    return 0;
}""")

priority_static = p4_3_2
def p5_1_1():
    """srtf_interactive"""
    _print_code(r"""#include<stdio.h>
// Practical 5.1.1: SRTF (Interactive)
int main() {
    int n, at[10], bt[10], rt[10], endTime, i, smallest, remain=0, time, sum_wait=0, sum_turnaround=0;
    printf("--- SRTF Interactive ---\n");
    printf("Tip: Try 3 procs: (AT 0, BT 7), (AT 2, BT 4), (AT 4, BT 1)\n");
    printf("Processes: "); scanf("%d",&n); remain=n;
    for(i=0;i<n;i++) { printf("P%d AT BT: ",i+1); scanf("%d %d",&at[i],&bt[i]); rt[i]=bt[i]; }
    rt[9]=9999;
    printf("\nExecution Log:\n");
    for(time=0;remain!=0;time++) {
        smallest=9;
        for(i=0;i<n;i++) if(at[i]<=time && rt[i]<rt[smallest] && rt[i]>0) smallest=i;
        rt[smallest]--;
        if(rt[smallest]==0) {
            remain--; endTime=time+1;
            sum_wait+=endTime-at[smallest]-bt[smallest];
            sum_turnaround+=endTime-at[smallest];
        }
    }
    printf("\nAvg WT = %.2f\nAvg TAT = %.2f\n",sum_wait*1.0/n,sum_turnaround*1.0/n);
    return 0;
}""")

srtf_interactive = p5_1_1
def p5_1_2():
    """srtf_static"""
    _print_code(r"""#include <stdio.h>
// Practical 5.1.2: SRTF (Static Hardcoded)
int main() {
    int n=4, i, t, AT[]={0,1,2,4}, BT[]={5,3,4,1}, rt[]={5,3,4,1}, complete=0, minm=9999, shortest=0, finish_time, check=0, wt[4], tat[4];
    float total_wt=0, total_tat=0;
    for(t=0; complete!=n; t++) {
        for(int j=0; j<n; j++) if((AT[j]<=t) && (rt[j]<minm) && rt[j]>0) { minm=rt[j]; shortest=j; check=1; }
        if(check==0) continue;
        rt[shortest]--; minm=rt[shortest];
        if(minm==0) minm=9999;
        if(rt[shortest]==0) {
            complete++; check=0; finish_time=t+1;
            wt[shortest] = finish_time-BT[shortest]-AT[shortest];
            if(wt[shortest]<0) wt[shortest]=0;
        }
    }
    printf("--- SRTF Static Mode (No Input Required) ---\n");
    printf("P\tAT\tBT\tTAT\tWT\n");
    for(i=0; i<n; i++) {
        tat[i]=BT[i]+wt[i]; total_wt+=wt[i]; total_tat+=tat[i];
        printf("P%d\t%d\t%d\t%d\t%d\n", i+1, AT[i], BT[i], tat[i], wt[i]);
    }
    printf("\nAvg TAT = %.2f\nAvg WT  = %.2f\n", total_tat/n, total_wt/n);
    return 0;
}""")

srtf_static = p5_1_2
def p5_2_1():
    """rr_interactive"""
    _print_code(r"""#include<stdio.h>
// Practical 5.2.1: Round Robin (Interactive)
int main() {
    int count,j,n,time,remain,flag=0,tq,wait_time=0,turnaround_time=0,at[10],bt[10],rt[10];
    printf("--- Round Robin Interactive ---\n");
    printf("Tip: Try 3 procs: (AT 0, BT 10), (AT 1, BT 5), (AT 2, BT 8) with TQ=2\n");
    printf("Processes: "); scanf("%d",&n); remain=n;
    for(count=0;count<n;count++) { printf("P%d AT BT: ",count+1); scanf("%d %d",&at[count],&bt[count]); rt[count]=bt[count]; }
    printf("Quantum: "); scanf("%d",&tq);
    printf("\nP\tTAT\tWT\n");
    for(time=0,count=0;remain!=0;) {
        if(rt[count]<=tq && rt[count]>0) { time+=rt[count]; rt[count]=0; flag=1; }
        else if(rt[count]>0) { rt[count]-=tq; time+=tq; }
        if(rt[count]==0 && flag==1) {
            remain--;
            printf("P[%d]\t%d\t%d\n",count+1,time-at[count],time-at[count]-bt[count]);
            wait_time+=time-at[count]-bt[count]; turnaround_time+=time-at[count];
            flag=0;
        }
        if(count==n-1) count=0;
        else if(at[count+1]<=time) count++;
        else count=0;
    }
    printf("\nAvg WT= %.2f\nAvg TAT= %.2f\n",wait_time*1.0/n,turnaround_time*1.0/n);
    return 0;
}""")

rr_interactive = p5_2_1
def p5_2_2():
    """rr_static"""
    _print_code(r"""#include <stdio.h>
// Practical 5.2.2: Round Robin (Static Hardcoded)
int main() {
    int n=4, AT[]={0,1,2,3}, BT[]={5,4,2,1}, rt[]={5,4,2,1}, TQ=2, remain=4, time=0, count=0, flag=0, wt=0, tat=0, total_wt=0, total_tat=0;
    printf("--- Round Robin Static (TQ=2) ---\n");
    printf("P\tTAT\tWT\n");
    while(remain!=0) {
        if(rt[count]<=TQ && rt[count]>0) { time+=rt[count]; rt[count]=0; flag=1; }
        else if(rt[count]>0) { rt[count]-=TQ; time+=TQ; }
        if(rt[count]==0 && flag==1) {
            remain--; tat=time-AT[count]; wt=tat-BT[count];
            printf("P%d\t%d\t%d\n", count+1, tat, wt);
            total_wt+=wt; total_tat+=tat; flag=0;
        }
        if(count==n-1) count=0;
        else if(AT[count+1]<=time) count++;
        else count=0;
    }
    printf("\nAvg TAT = %.2f\nAvg WT  = %.2f\n", (float)total_tat/n, (float)total_wt/n);
    return 0;
}""")

rr_static = p5_2_2
def p7_1():
    """bankers_interactive"""
    _print_code(r"""#include <stdio.h>
// Practical 7.1: Bankers (Interactive)
int main() {
    int n, m, i, j, k, alloc[10][10], max[10][10], avail[10], f[10], ans[10], ind=0, need[10][10];
    printf("--- Bankers Algorithm Interactive ---\n");
    printf("Tip: Try 3 processes, 3 resources. Be careful entering the matrices.\n");
    printf("Processes: "); scanf("%d", &n);
    printf("Resources: "); scanf("%d", &m);
    printf("Alloc Matrix:\n"); for(i=0;i<n;i++) for(j=0;j<m;j++) scanf("%d", &alloc[i][j]);
    printf("Max Matrix:\n"); for(i=0;i<n;i++) for(j=0;j<m;j++) scanf("%d", &max[i][j]);
    printf("Available:\n"); for(i=0;i<m;i++) scanf("%d", &avail[i]);
    for(k=0;k<n;k++) f[k]=0;
    for(i=0;i<n;i++) for(j=0;j<m;j++) need[i][j]=max[i][j]-alloc[i][j];
    for(k=0;k<5;k++) for(i=0;i<n;i++) if(f[i]==0) {
        int flag=0;
        for(j=0;j<m;j++) if(need[i][j]>avail[j]) { flag=1; break; }
        if(flag==0) { ans[ind++]=i; for(int y=0;y<m;y++) avail[y]+=alloc[i][y]; f[i]=1; }
    }
    printf("Safe Sequence: "); for(i=0;i<n;i++) printf("P%d ", ans[i]);
    return 0;
}""")

bankers_interactive = p7_1
def p7_2():
    """bankers_static"""
    _print_code(r"""#include <stdio.h>
// Practical 7.2: Bankers (Static Hardcoded)
int main() {
    int A[5][3]={{0,1,0},{2,0,0},{3,0,2},{2,1,1},{0,0,2}};
    int M[5][3]={{7,5,3},{3,2,2},{9,0,2},{2,2,2},{4,3,3}};
    int N[5][3]={{7,4,3},{1,2,2},{6,0,0},{0,1,1},{4,3,1}};
    int S[5]={1,3,4,0,2};
    printf("--- Bankers Algorithm Static Mode ---\n");
    printf("P   Alloc\tMax\t\tNeed\n");
    for(int i=0;i<5;i++)
        printf("P%d  %d %d %d\t%d %d %d\t%d %d %d\n", i, A[i][0],A[i][1],A[i][2], M[i][0],M[i][1],M[i][2], N[i][0],N[i][1],N[i][2]);
    printf("\nSafe Sequence: "); for(int i=0;i<5;i++) printf("P%d ", S[i]);
    return 0;
}""")

bankers_static = p7_2
def p8_1():
    """dining_interactive"""
    _print_code(r"""#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
// Practical 8.1: Dining Philosophers (Interactive)
sem_t chopstick[5];
int philosophers[5] = {0,1,2,3,4};
void *func(void *n) {
    int ph = *(int *)n;
    printf("Philosopher %d thinking\n", ph + 1);
    sem_wait(&chopstick[ph]);
    printf("Philosopher %d takes stick %d\n", ph + 1, ph + 1);
    sem_wait(&chopstick[(ph + 1) % 5]);
    printf("Philosopher %d takes stick %d\n", ph + 1, (ph + 1) % 5 + 1);
    printf("Philosopher %d eating\n", ph + 1);
    sleep(1);
    printf("Philosopher %d drops sticks %d & %d\n", ph + 1, ph+1, (ph + 1) % 5 + 1);
    sem_post(&chopstick[(ph + 1) % 5]);
    sem_post(&chopstick[ph]);
    return NULL;
}
int main() {
    int i, n=5;
    printf("--- Dining Philosophers (Threaded) ---\n");
    printf("Note: Requires -lpthread to compile.\n");
    pthread_t t[5];
    for (i=0; i<5; i++) sem_init(&chopstick[i], 0, 1);
    for (i=0; i<5; i++) pthread_create(&t[i], NULL, func, &philosophers[i]);
    for (i=0; i<5; i++) pthread_join(t[i], NULL);
    return 0;
}""")

dining_interactive = p8_1
def p8_2():
    """dining_static"""
    _print_code(r"""#include <stdio.h>
// Practical 8.2: Dining Philosophers (Static Table)
int main() {
    char *S[5][5] = {
        {"E","T","T","T","T"},
        {"T","E","T","T","T"},
        {"T","T","E","T","T"},
        {"T","T","T","E","T"},
        {"T","T","T","T","E"}
    };
    printf("--- Dining Philosophers Static Table ---\n");
    printf("Round  P0  P1  P2  P3  P4\n");
    for (int i=0;i<5;i++) {
        printf("  %d    ", i+1);
        for (int j=0;j<5;j++) printf("%s   ", S[i][j]);
        printf("\n");
    }
    return 0;
}""")

dining_static = p8_2
def p9_1_1():
    """fifo_interactive"""
    _print_code(r"""#include<stdio.h>
// Practical 9.1.1: FIFO (Interactive)
int main() {
    int i, j=0, n, a[50], frame[10], no, k, avail, count=0;
    printf("--- FIFO Page Replacement Interactive ---\n");
    printf("Tip: Try 5 pages, Ref String: 1 2 3 1 4, Frames: 3\n");
    printf("Num Pages: "); scanf("%d",&n);
    printf("Ref String: "); for(i=0;i<n;i++) scanf("%d",&a[i]);
    printf("Num Frames: "); scanf("%d",&no);
    for(i=0;i<no;i++) frame[i]=-1;
    printf("\tRef\tFrames\n");
    for(i=0;i<n;i++) {
        printf("%d\t", a[i]); avail=0;
        for(k=0;k<no;k++) if(frame[k]==a[i]) avail=1;
        if(avail==0) {
            frame[j]=a[i]; j=(j+1)%no; count++;
            for(k=0;k<no;k++) printf("%d ", frame[k]);
        }
        printf("\n");
    }
    printf("Page Faults: %d\n", count);
    return 0;
}""")

fifo_interactive = p9_1_1
def p9_1_2():
    """fifo_static"""
    _print_code(r"""#include <stdio.h>
// Practical 9.1.2: FIFO (Static Hardcoded)
int main() {
    int RS[7] = {1,2,3,4,1,2,5}, F1[7]={1,1,1,4,4,4,5}, F2[7]={-1,2,2,2,1,1,1}, F3[7]={-1,-1,3,3,3,2,2};
    char PF[7]={'F','F','F','F','F','F','F'};
    int i, faults = 0;
    printf("--- FIFO Static Mode ---\n");
    printf("Ref  F1  F2  F3  PF\n");
    for(i=0;i<7;i++) {
        printf("%3d %3d %3d %3d  %c\n", RS[i], F1[i], F2[i], F3[i], PF[i]);
        if (PF[i]=='F') faults++;
    }
    printf("Total Page Faults = %d\n", faults);
    return 0;
}""")

fifo_static = p9_1_2
def p9_2_1():
    """lru_interactive"""
    _print_code(r"""#include<stdio.h>
// Practical 9.2.1: LRU (Interactive)
int findLRU(int time[], int n) {
    int i, minimum=time[0], pos=0;
    for(i=1;i<n;++i) if(time[i]<minimum) { minimum=time[i]; pos=i; }
    return pos;
}
int main() {
    int no_of_frames, no_of_pages, frames[10], pages[30], counter=0, time[10], flag1, flag2, i, j, pos, faults=0;
    printf("--- LRU Page Replacement Interactive ---\n");
    printf("Tip: Try Frames: 3, Pages: 5, Ref String: 1 2 3 1 4\n");
    printf("Frames: "); scanf("%d",&no_of_frames);
    printf("Pages: "); scanf("%d",&no_of_pages);
    printf("Ref String: "); for(i=0;i<no_of_pages;++i) scanf("%d",&pages[i]);
    for(i=0;i<no_of_frames;++i) frames[i]=-1;
    for(i=0;i<no_of_pages;++i) {
        flag1=flag2=0;
        for(j=0;j<no_of_frames;++j) if(frames[j]==pages[i]) { counter++; time[j]=counter; flag1=flag2=1; break; }
        if(flag1==0) {
            for(j=0;j<no_of_frames;++j) if(frames[j]==-1) { counter++; faults++; frames[j]=pages[i]; time[j]=counter; flag2=1; break; }
        }
        if(flag2==0) { pos=findLRU(time, no_of_frames); counter++; faults++; frames[pos]=pages[i]; time[pos]=counter; }
    }
    printf("\nTotal Faults = %d\n", faults);
    return 0;
}""")

lru_interactive = p9_2_1
def p9_2_2():
    """lru_static"""
    _print_code(r"""#include <stdio.h>
// Practical 9.2.2: LRU (Static Hardcoded)
int main() {
    int RS[7] = {1,2,3,4,1,2,5}, F1[7]={1,1,1,4,4,4,5}, F2[7]={-1,2,2,2,1,1,1}, F3[7]={-1,-1,3,3,3,2,2};
    char PF[7]={'F','F','F','F','F','F','F'};
    int i, faults = 0;
    printf("--- LRU Static Mode ---\n");
    printf("Ref  F1  F2  F3  PF\n");
    for(i=0;i<7;i++) {
        printf("%3d %3d %3d %3d  %c\n", RS[i], F1[i], F2[i], F3[i], PF[i]);
        if (PF[i]=='F') faults++;
    }
    printf("Total Page Faults = %d\n", faults);
    return 0;
}""")

lru_static = p9_2_2
def p9_3_1():
    """optimal_interactive"""
    _print_code(r"""#include<stdio.h>
// Practical 9.3.1: Optimal (Interactive)
int main() {
    int frames[10], pages[30], temp[10], flag1, flag2, i, j, k, pos, max, faults=0, no_of_frames, no_of_pages;
    printf("--- Optimal Page Replacement Interactive ---\n");
    printf("Tip: Try Frames: 3, Pages: 5, Ref String: 1 2 3 1 4\n");
    printf("Frames: "); scanf("%d",&no_of_frames);
    printf("Pages: "); scanf("%d",&no_of_pages);
    printf("Ref String: "); for(i=0;i<no_of_pages;++i) scanf("%d",&pages[i]);
    for(i=0;i<no_of_frames;++i) frames[i]=-1;
    for(i=0;i<no_of_pages;++i) {
        flag1=flag2=0;
        for(j=0;j<no_of_frames;++j) if(frames[j]==pages[i]) { flag1=flag2=1; break; }
        if(flag1==0) {
            for(j=0;j<no_of_frames;++j) if(frames[j]==-1) { faults++; frames[j]=pages[i]; flag2=1; break; }
        }
        if(flag2==0) {
            for(j=0;j<no_of_frames;++j) { temp[j]=-1; for(k=i+1;k<no_of_pages;++k) if(frames[j]==pages[k]) { temp[j]=k; break; } }
            for(j=0;j<no_of_frames;++j) if(temp[j]==-1) { pos=j; flag2=1; break; }
            if(flag2==0) { max=temp[0]; pos=0; for(j=1;j<no_of_frames;++j) if(temp[j]>max) { max=temp[j]; pos=j; } }
            frames[pos]=pages[i]; faults++;
        }
    }
    printf("\nTotal Faults = %d\n", faults);
    return 0;
}""")

optimal_interactive = p9_3_1
def p9_3_2():
    """optimal_static"""
    _print_code(r"""#include <stdio.h>
// Practical 9.3.2: Optimal (Static Hardcoded)
int main() {
    int RS[7]={1,2,3,4,1,2,5}, F1[7]={1,1,1,1,1,1,1}, F2[7]={-1,2,2,2,2,2,2}, F3[7]={-1,-1,3,4,4,4,5};
    char PF[7]={'F','F','F','F',' ',' ','F'};
    int i, faults = 0;
    printf("--- Optimal Static Mode ---\n");
    printf("Ref  F1  F2  F3  PF\n");
    for(i=0;i<7;i++) {
        printf("%3d %3d %3d %3d  %c\n", RS[i], F1[i], F2[i], F3[i], PF[i]);
        if (PF[i]=='F') faults++;
    }
    printf("Total Page Faults = %d\n", faults);
    return 0;
}""")

optimal_static = p9_3_2
