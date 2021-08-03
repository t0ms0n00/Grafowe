#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <limits.h>

typedef struct Edge{
    int edge_from;  /// poczatek
    int edge_to;     /// koniec
    int cost;      /// lapowka
    struct Edge * next;
} Edge;

void addEdge(Edge **f, int winner, int loser, int cost){
    Edge *rob;
    rob=malloc(sizeof(Edge));
    rob->edge_from=winner;
    rob->edge_to=loser;
    rob->cost=cost;
    rob->next=(*f);
    *f=rob;
}

void printNeighbours(Edge *f){
    if(f==NULL) return;
    Edge *pom=f;
    while (pom!=NULL){
        printf("from: %d to: %d cost: %d\n", pom->edge_from,pom->edge_to,pom->cost);
        pom=pom->next;
    }
}

bool existEdge(Edge **f,int to){
    Edge *pom=(*f);
    while(pom!=NULL && pom->edge_to!=to) pom=pom->next;
    if(pom!=NULL) return true;
    return false;
}

void removeEdge(Edge **f,int to){
    Edge *pom=(*f);
    Edge *prev=NULL;
    while(pom!=NULL && pom->edge_to!=to){
        prev=pom;
        pom=pom->next;
    }
    if(pom==NULL) return;
    if(pom==(*f)){
        Edge *tmp=NULL;
        if (*f!=NULL){
            tmp=(*f)->next;
            free(*f);
            *f=tmp;
        }
    }
    else{
        prev->next=pom->next;
        free(pom);
    }
}

Edge* getEdge(Edge **f,int to){
    Edge *pom=(*f);
    while(pom!=NULL && pom->edge_to!=to) pom=pom->next;
    if(pom!=NULL) return pom;
    return NULL;
}

int countEdges(Edge **f){
    int count=0;
    Edge *pom=(*f);
    while(pom!=NULL){
        count++;
        pom=pom->next;
    }
    return count;
}

int setMKingGames(Edge **graph,int n,int wins[n],int m){
    int cost=0;
    int setted=0;
    int k=0;
    while (setted!=m && k<n){
        if(existEdge(&graph[k],0)){
            ///printf("Ustawiam mecz z %d\n",k);
            wins[k]-=1;
            wins[0]+=1;
            int val=getEdge(&graph[k],0)->cost;
            removeEdge(&graph[k],0);
            addEdge(&graph[0],0,k,-val);
            setted+=1;
        }
        k+=1;
    }
    if(setted!=m && n==k) printf("WYKRYTY BLAD PRZY GRAFIE ____________________________________________________________\n");
    bool toset[n];
    toset[0]=false;
    for(int i=1;i<n;i++){
        toset[i]=true;
    }
    int mini=n;
    int vtoset=0;
    while(true){
        mini=wins[0];
        vtoset=0;
        for(int i=0;i<n;i++){
            if(toset[i] && wins[i]<mini){
                vtoset=i;
                mini=wins[i];
            }
        }
        if(vtoset==0) break;
        for(int j=1;j<n;j++){
            if(wins[vtoset]==wins[0]) break;
            if(toset[j] && existEdge(&graph[j],vtoset)){
                wins[j]-=1;
                wins[vtoset]+=1;
                int val=getEdge(&graph[j],vtoset)->cost;
                removeEdge(&graph[j],vtoset);
                addEdge(&graph[vtoset],vtoset,j,-val);
            }
        }
        toset[vtoset]=false;
    }
    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            if(existEdge(&graph[i],j)){
                int val=getEdge(&graph[i],j)->cost;
                if(val<0) cost+=val;
            }
        }
    }
    cost=cost*(-1);
    return cost;
}

void unsetAll(Edge **graph,int n,int wins[n]){
    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            if(existEdge(&graph[i],j)){
                int val=getEdge(&graph[i],j)->cost;
                if(val<0){
                    removeEdge(&graph[i],j);
                    addEdge(&graph[j],j,i,-val);
                }
            }
        }
    }
    for(int i=0;i<n;i++){
        int count=0;
        Edge *e=graph[i];
        while(e!=NULL){
            count+=1;
            e=e->next;
        }
        wins[i]=count;
    }
}

void DFS(Edge** res,int start,int end, int resSize, bool visited[resSize], int parent[resSize]){
    visited[start]=true;
    Edge* act=res[start];
    while (act!=NULL){
        if(!visited[act->edge_to]){
            parent[act->edge_to]=start;
            DFS(res,act->edge_to,end,resSize,visited,parent);
        }
        act=act->next;
    }
}

void Ford_Fulkerson(Edge** res,int start,int end, int resSize){
    while(true){
        bool visited[resSize];
        int parent[resSize];
        for(int i=0;i<resSize;i++){
            visited[i]=false;
            parent[i]=-1;
        }
        DFS(res,start,end,resSize,visited,parent);
        int back=end;
        while(parent[back]!=-1){
            back=parent[back];
        }
        if(back!=start) break;
        back=end;
        while(parent[back]!=-1){        /// przebudowanie sieci residualnej
            addEdge(&res[back],back,parent[back],-1*getEdge(&res[parent[back]],back)->cost);
            removeEdge(&res[parent[back]],back);
            back=parent[back];
        }
    }
}

bool isNegativeCycle(Edge** res,int resSize,int begin){
    int parents[resSize];
    int d[resSize];
    for(int i=0;i<resSize;i++){
        parents[i]=-1;
        d[i]=INT_MAX;
    }
    d[begin]=0;
    for(int i=0;i<resSize-1;i++){       /// relaksacja
        for(int j=0;j<resSize;j++){
            Edge *e=res[j];
            while(e!=NULL){
                if(d[e->edge_from] != INT_MAX && d[e->edge_to]>d[e->edge_from]+e->cost){
                    d[e->edge_to]=d[e->edge_from]+e->cost;
                    parents[e->edge_to]=e->edge_from;
                }
                e=e->next;
            }
        }
    }
    bool used[resSize];
    for(int j=0;j<resSize;j++){         /// weryfikacja
        Edge *e=res[j];
        while(e!=NULL){
            if(d[e->edge_from]!=INT_MAX && d[e->edge_to]>d[e->edge_from]+e->cost){  /// mamy cykl ujemny, update sieci wzdluz cyklu
                int back=e->edge_from;
                int counter=1;
                int *cycle=malloc(counter*sizeof(int));
                cycle[counter-1]=back;
                for(int i=0;i<resSize;i++){
                    used[i]=false;
                }
                while(!used[back]){
                    used[back]=true;
                    counter+=1;
                    cycle=realloc(cycle,counter*sizeof(int));
                    cycle[counter-1]=parents[back];
                    back=parents[back];
                }
                int c=0;
                while(cycle[c]!=cycle[counter-1]) c++;
                int tab[counter-c];
                for(int k=0;k<counter-c;k++){
                    tab[k]=cycle[c+k];
                }
                for(int k=0;k<counter-c-1;k++){
                    addEdge(&res[tab[k]],tab[k],tab[k+1],-1*getEdge(&res[tab[k+1]],tab[k])->cost);
                    removeEdge(&res[tab[k+1]],tab[k]);
                }
                free(cycle);
                return true;
            }
            e=e->next;
        }
    }
    return false;
}

int minCostMaxFlow(Edge** res,Edge **graph,int start, int end, int resSize){
    Ford_Fulkerson(res,start,end,resSize);
    for(int i=0;i<resSize;i++) while(isNegativeCycle(res,resSize,i));
    int reduction=0;
    for(int i=0;i<start-2;i++){
        Edge* e=res[i];
        while(e!=NULL){
            if(!existEdge(&graph[i],e->edge_to) && e->edge_to<start-2){       /// update grafu
                reduction+=getEdge(&res[i],e->edge_to)->cost;
                addEdge(&graph[e->edge_from],e->edge_from,e->edge_to,e->cost);
                removeEdge(&graph[e->edge_to],e->edge_from);
            }
            e=e->next;
        }
    }
    return reduction;
}

bool isPossible(Edge **graph,int n,int wins[n],int actCost,int budget){
    while(true){
        if(actCost<=budget) return true;
        Edge **Residual=malloc((n+3)*sizeof(Edge*));
        for(int i=0;i<n+3;i++){
            Residual[i]=malloc(sizeof(Edge));
            Residual[i]=NULL;
        }
        for(int i=0;i<n;i++){
            Edge *e=graph[i];
            while(e!=NULL){
                addEdge(&Residual[i],i,e->edge_to,e->cost);
                e=e->next;
            }
        }
        for(int i=1;i<n;i++){
            if (wins[i]>0){
                addEdge(&Residual[n],n,i,0);    /// hiperZrodlo
            }
        }
        for(int i=1;i<n;i++){
            if (wins[0]!=wins[i]){
                addEdge(&Residual[i],i,n+1,0); /// hiperUjscie
            }
        }
        addEdge(&Residual[n+2],n+2,n,0);
        int reduction=minCostMaxFlow(Residual,graph,n+2,n+1,n+3);
        if(reduction<=0) {
            ///printf("Zeszlo do %d\n",actCost);
            for(int j=0;j<n+3;j++){
                Edge* e=Residual[j];
                while(e!=NULL){
                    removeEdge(&Residual[j],e->edge_to);
                    e=e->next;
                }
                free(Residual[j]);
            }
            free(Residual);
            return false;
        }
        actCost=actCost-reduction;
        for(int i=1;i<n;i++){
            wins[i]=countEdges(&graph[i]);
        }
        for(int j=0;j<n+3;j++){
            Edge* e=Residual[j];
            while(e!=NULL){
                removeEdge(&Residual[j],e->edge_to);
                e=e->next;
            }
            free(Residual[j]);
        }
        free(Residual);
    }
}

int main(){
    int T; /// liczba zestawow
    scanf("%d",&T);
    int B,n,x,y,w,b;
    for (int t=0;t<T;t++){
        ///printf("ZESTAW %d\n",t);
        scanf("%d",&B);
        scanf("%d",&n);
        Edge **Graph=malloc(n*sizeof(Edge*));
        for(int i=0;i<n;i++){
            Graph[i]=malloc(sizeof(Edge));
            Graph[i]=NULL;
        }
        int* wins=malloc(n*sizeof(int));                        /// kto ile wygranych
        for(int j=0;j<n;j++){
            wins[j]=0;
        }
        for(int j=0;j<n*(n-1)/2;j++){       /// stworz graf
            scanf("%d %d %d %d",&x,&y,&w,&b);
            if(b>0 || w!=0){
                if(x==w){
                    addEdge(&Graph[x],x,y,b);
                }
                else{
                    addEdge(&Graph[y],y,x,b);
                }
            }
            wins[w]++;
        }
        int clearwins=wins[0];
        bool possible=false;
        for(int x=0;x<n-clearwins;x++){
            /*if(x<=0){               /// do poprawy
                possible=true;
                break;
            }*/
            if((x+clearwins)*n*2<(n*(n-1))) continue;
            int actCost=setMKingGames(Graph,n,wins,x);
            ///printf("Dzialamy na %d wygranych\n",x+clearwins);
            ///printf("TEST Wygranych\n");
            /*printf("STAN GRAFU PRZY %d WYGRANYCH KROLA\n",x+clearwins);
            for(int i=0;i<n;i++){
                printf("%d wygrywa %d\n",i,wins[i]);
                printNeighbours(Graph[i]);
            }*/
            if(isPossible(Graph,n,wins,actCost,B)){
                possible=true;
                unsetAll(Graph,n,wins);
                break;
            }
            unsetAll(Graph,n,wins);
            wins[0]=clearwins;
            /*printf("STAN GRAFU PO POWROCIE DO DEFAULT\n");
            for(int i=0;i<n;i++){
                printf("%d wygrywa %d\n",i,wins[i]);
                printNeighbours(Graph[i]);
            }*/
            ///printf("------------------------------------------------------------\n");
        }
        if(possible) printf("TAK\n");
        else printf("NIE\n");
        /*for(int i=0;i<n;i++){
            printf("%d wygral %d\n",i,wins[i]);
            printNeighbours(Graph[i]);
        }*/
        for(int j=0;j<n;j++){
            Edge *e=Graph[j];
            while(e!=NULL){
                removeEdge(&Graph[j],e->edge_to);
                e=e->next;
            }
            free(Graph[j]);
        }
        free(Graph);
        free(wins);
    }
    return 0;
}
