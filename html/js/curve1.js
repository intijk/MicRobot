function Curve() {
};

Curve.prototype.points=new Array();
Curve.prototype.curvePoints=function(type){
	if(!type){
		var type=="CatMull-Rom";
	}
	if(type=="CatMull-Rom"){
		var pList=[];
		if(this.points.length<2){
			return pList;
		}
		for(i=0;i<this.points.length-1;i++){
			var C0=this.points[i];
			var C1=this.points[i+1];
			var D0,D1;
			if(i==0){
				D0=C0;
			}else{
				D0=this.points[i-1];
			}
			if(i>=this.points.length-2){
				D1=C1;
			}else{
				D1=this.points[i+2];
			}
			//M=0.5*numpy.matrix([[-1,3,-3,1],[2,-5,4,-1],[-1,0,1,0],[0,2,0,0]])
			var M=THREE.Matrix4(-1,3,-3,1,2,-5,4,-1,-1,0,1,0,0,2,0,0);	
			M.multiplyScalar(0.5);
			//G=numpy.matrix([D0,C0,C1,D1])
			var G=THREE.Matrix4(D0.x,D0.y,C0.x,C0.y,C1.x,C1.y,D1.x,D1.y);
			var MG=M.multiply(G);
			
//		t=[]	
			var t=new Array();
			var step=0.1;
			for(i=0;i<1;i++){
				t.push(i);
			}
			t.push(1);
			for(i=0;i<t.length;i++){
				var T=THREE.Vector4(t[i]*t[i]*t[i],t[i]*t[i],t[i],1);
				T.applyMatrix4(MG);
				pList.push(new THREE.Vector2(T.x,T.y));
			}
		}
		return pList;
	}
}

