/* Erdos 642: G "iyi" <=> her cevrimde kiris sayisi < kose sayisi
   <=> Hamilton cevrimi olan her S kose kumesi icin e(G[S]) <= 2|S|-1.
   stdin: graph6 (n <= 20). stdout: iyi cizgeler. stderr: sayim.
   Secenek: -q yalniz sayar; -v kotu cizgeler icin tanik S yazar. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint32_t u32;
static int n; static u32 adj[20];
static inline int pc(u32 x){return __builtin_popcount(x);}

static u32 S_; static int s_; static int start_;
static int dfs(int v, u32 vis, int cnt){
    if(cnt==s_) return (adj[v]>>start_)&1;
    u32 rem = S_ & ~vis;
    /* budama: kalan her kosenin, kalanlar+v+start icinde en az 2 komsusu olmali */
    u32 cand = adj[v] & rem;
    if(!cand) return 0;
    for(u32 r=rem; r; r&=r-1){
        int w=__builtin_ctz(r);
        u32 nb = adj[w] & (rem | (1u<<v) | (1u<<start_));
        if(pc(nb)<2) return 0;
    }
    while(cand){
        int w=__builtin_ctz(cand); cand&=cand-1;
        if(dfs(w, vis|(1u<<w), cnt+1)) return 1;
    }
    return 0;
}
static int hamilton(u32 S){
    int s=pc(S); if(s<3) return 0;
    for(u32 r=S;r;r&=r-1){int w=__builtin_ctz(r); if(pc(adj[w]&S)<2) return 0;}
    /* en dusuk dereceli koseden basla */
    int best=-1,bd=99;
    for(u32 r=S;r;r&=r-1){int w=__builtin_ctz(r); int d=pc(adj[w]&S); if(d<bd){bd=d;best=w;}}
    S_=S; s_=s; start_=best;
    return dfs(best, 1u<<best, 1);
}
/* doner: 0 = iyi, aksi halde tanik S */
static u32 kotu_tanik(void){
    u32 full=(n==32)?0xffffffffu:((1u<<n)-1);
    /* once tum kume, sonra buyukten kucuge degil: dogal sira yeterli */
    int etot=0; for(int i=0;i<n;i++) etot+=pc(adj[i]); etot/=2;
    if(etot>=2*n && hamilton(full)) return full;
    for(u32 S=1; S<=full && S; S++){
        int s=pc(S); if(s<5 || S==full) continue;
        int e=0; for(u32 r=S;r;r&=r-1){int w=__builtin_ctz(r); e+=pc(adj[w]&S);} e/=2;
        if(e>=2*s && hamilton(S)) return S;
    }
    return 0;
}
int main(int argc,char**argv){
    int quiet=0, verbose=0;
    for(int i=1;i<argc;i++){ if(!strcmp(argv[i],"-q")) quiet=1; if(!strcmp(argv[i],"-v")) verbose=1; }
    char line[256]; long tot=0, good=0; int maxfazla=-999; static long hist[21][200];
    while(fgets(line,sizeof line,stdin)){
        if(line[0]=='>'||line[0]=='\n') continue;
        n=line[0]-63; if(n>20){fprintf(stderr,"n>20\n");return 1;}
        memset(adj,0,sizeof adj);
        int k=0; const char*p=line+1; int bit=0, cur=0;
        for(int j=1;j<n;j++) for(int i=0;i<j;i++){
            if(bit==0){cur=*p++-63; bit=6;}
            bit--; if((cur>>bit)&1){adj[i]|=1u<<j; adj[j]|=1u<<i;}
            k++;
        }
        tot++;
        u32 w=kotu_tanik();
        if(!w){ good++;
            u32 full=(1u<<n)-1; int c=0, e=0;
            for(int i=0;i<n;i++) e+=pc(adj[i]); e/=2;
            for(u32 S=full; S; S--){ int sz=pc(S); if(sz<=c||sz<3) continue; if(hamilton(S)) c=sz; }
            int fazla = e - (3*n - c - 1);
            if(fazla>maxfazla) maxfazla=fazla;
            hist[c][e]++;
            if(fazla>=0){ line[strcspn(line,"\n")]=0; printf("%s n=%d e=%d c=%d excess=%d\n",line,n,e,c,fazla); }
        }
        else if(verbose){ line[strcspn(line,"\n")]=0; printf("%s BAD S=0x%x |S|=%d\n",line,w,pc(w)); }
    }
    fprintf(stderr,"total=%ld good=%ld max_excess=%d\n",tot,good,maxfazla);
    for(int c=0;c<=20;c++){ int me=-1; for(int e=0;e<200;e++) if(hist[c][e]) me=e; if(me>=0) fprintf(stderr,"  c=%d maxe=%d (adet %ld)\n",c,me,hist[c][me]); }
    return 0;
}
