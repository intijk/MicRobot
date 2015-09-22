function Curve() {
	this.points=new Array();
	this.pointRadius=0.03;
	this.curveLine=null;
	this.curvePoints=new THREE.Object3D();
};
Curve.prototype.updateLine=function(){
	var curveGeo=new THREE.Geometry();
	curveGeo.vertices=this.getCurvePoints();
	this.curveLine=new THREE.Line(curveGeo,new THREE.LineBasicMaterial({color:0xea892a,linewidth:2}));
};

Curve.prototype.updatePoints=function(){
	this.curvePoints.children=[];
	for(i=0;i<this.points.length;i++){
		var sphere=new THREE.Mesh(new THREE.SphereGeometry(0.03, 24, 24 ),new THREE.MeshBasicMaterial( { color: 0xe32429,overdraw:true } ));
		sphere.position.x=this.points[i].x;
		sphere.position.y=0;
		sphere.position.z=this.points[i].y;
		this.curvePoints.add(sphere);
	}
};
Curve.prototype.draw=function(scene){
	scene.remove(this.curvePoints);
	scene.remove(this.curveLine);
	this.updateLine();
	this.updatePoints();
	scene.add(this.curveLine);
	scene.add(this.curvePoints);
};

Curve.prototype.getPointAt=function(length){
		var M=new THREE.Matrix4(-0.5,1.5,-1.5,0.5,1,-2.5,2,-0.5,-0.5,0,0.5,0,0,1,0,0);
		var pList=[];
		var Mm,G,T,e,x,y,i,j,step,C0,C1,D0,D1,currentPos,currentL=0,prevPos,prevL=0,sumL=0;
		if(this.points.length<2){
			return 0;
		}
		currentPos=this.points[0].clone();
		currentL=0.0;
		prevPos=currentPos.clone();
		prevL=0.0;
		for(i=0;i<this.points.length-1;i++){
			C0=this.points[i];
			C1=this.points[i+1];
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

			Mm=M.clone();
			//G=numpy.matrix([D0,C0,C1,D1])
			G=new THREE.Matrix4(
					D0.x,D0.y,0,0,
					C0.x,C0.y,0,0,
					C1.x,C1.y,0,0,
					D1.x,D1.y,0,0);
			MG=Mm.multiply(G);
			t=[];
			step=0.01;
			for(j=0;j<1;j+=step){
				t.push(j);
			}
			t.push(1);
			for(j=0;j<t.length;j++){
				T=new THREE.Vector4(t[j]*t[j]*t[j],t[j]*t[j],t[j],1);
				//T.applyMatrix4(MG);
				e=MG.elements;
				x=T.x*e[0]+T.y*e[1]+T.z*e[2]+T.w*e[3];
				y=T.x*e[4]+T.y*e[5]+T.z*e[6]+T.w*e[7];
				

				prevL=currentL;
				currentL+=Math.sqrt((currentPos.x-prevPos.x)*(currentPos.x-prevPos.x)+(currentPos.y-prevPos.y)*(currentPos.y-prevPos.y))
				prevPos.copy(currentPos);
				currentPos.set(x,y);
				if(currentL>=length){
					if(length-prevL>currentL-length){
						return currentPos;
					}else{
						return prevPos;
					}
				}
			}
		}
		return sumL;
};
Curve.prototype.getLength=function(){
		var M=new THREE.Matrix4(-0.5,1.5,-1.5,0.5,1,-2.5,2,-0.5,-0.5,0,0.5,0,0,1,0,0);
		var pList=[];
		var Mm,G,T,e,x,y,i,j,step,C0,C1,D0,D1,currentPos,currentL=0,prevPos,prevL=0,sumL=0;
		if(this.points.length<2){
			return 0;
		}
		currentPos=this.points[0].clone();
		currentL=0.0;
		prevPos=currentPos.clone();
		prevL=0.0;
		for(i=0;i<this.points.length-1;i++){
			C0=this.points[i];
			C1=this.points[i+1];
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

			Mm=M.clone();
			//G=numpy.matrix([D0,C0,C1,D1])
			G=new THREE.Matrix4(
					D0.x,D0.y,0,0,
					C0.x,C0.y,0,0,
					C1.x,C1.y,0,0,
					D1.x,D1.y,0,0);
			MG=Mm.multiply(G);
			t=[];
			step=0.01;
			for(j=0;j<1;j+=step){
				t.push(j);
			}
			t.push(1);
			for(j=0;j<t.length;j++){
				T=new THREE.Vector4(t[j]*t[j]*t[j],t[j]*t[j],t[j],1);
				//T.applyMatrix4(MG);
				e=MG.elements;
				x=T.x*e[0]+T.y*e[1]+T.z*e[2]+T.w*e[3];
				y=T.x*e[4]+T.y*e[5]+T.z*e[6]+T.w*e[7];
				
				prevPos.copy(currentPos);
				currentPos.set(x,y);
				sumL+=Math.sqrt((currentPos.x-prevPos.x)*(currentPos.x-prevPos.x)+(currentPos.y-prevPos.y)*(currentPos.y-prevPos.y))
			}
		}
		return sumL;
}
Curve.prototype.getCurvePoints=function(type){
	if(!type){
		var type="CatMull-Rom";
	}
	if(type=="CatMull-Rom"){
		var M=new THREE.Matrix4(-0.5,1.5,-1.5,0.5,1,-2.5,2,-0.5,-0.5,0,0.5,0,0,1,0,0);
		var pList=[];
		var Mm,G,T,e,x,y,i,j,step,C0,C1,D0,D1;
		if(this.points.length<2){
			pList.push(new THREE.Vector3(0,0,0));
			return pList;
		}
		for(i=0;i<this.points.length-1;i++){
			C0=this.points[i];
			C1=this.points[i+1];
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

			Mm=M.clone();
			//G=numpy.matrix([D0,C0,C1,D1])
			G=new THREE.Matrix4(
					D0.x,D0.y,0,0,
					C0.x,C0.y,0,0,
					C1.x,C1.y,0,0,
					D1.x,D1.y,0,0);
			MG=Mm.multiply(G);
			t=[];
			step=0.1;
			for(j=0;j<1;j+=step){
				t.push(j);
			}
			t.push(1);
			for(j=0;j<t.length;j++){
				T=new THREE.Vector4(t[j]*t[j]*t[j],t[j]*t[j],t[j],1);
				//T.applyMatrix4(MG);
				e=MG.elements;
				x=T.x*e[0]+T.y*e[1]+T.z*e[2]+T.w*e[3];
				y=T.x*e[4]+T.y*e[5]+T.z*e[6]+T.w*e[7];

				pList.push(new THREE.Vector3(x,0,y));
			}
		}
		return pList;
	}
};
Curve.prototype.isXAsc=function(type){
	if(!type){
		var type="CatMull-Rom";
	}
	if(type=="CatMull-Rom"){
		var M=new THREE.Matrix4(-0.5,1.5,-1.5,0.5,1,-2.5,2,-0.5,-0.5,0,0.5,0,0,1,0,0);
		var pList=[];
		var Mm,G,T,e,x,y,i,j,step,C0,C1,D0,D1;
		if(this.points.length<2){
			return true;
		}
		var mostRight=-9e100;
		for(i=0;i<this.points.length-1;i++){
			C0=this.points[i];
			C1=this.points[i+1];
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

			Mm=M.clone();
			//G=numpy.matrix([D0,C0,C1,D1])
			G=new THREE.Matrix4(
					D0.x,D0.y,0,0,
					C0.x,C0.y,0,0,
					C1.x,C1.y,0,0,
					D1.x,D1.y,0,0);
			MG=Mm.multiply(G);
			t=[];
			step=0.1;
			for(j=0;j<1;j+=step){
				t.push(j);
			}
			t.push(1);
			for(j=0;j<t.length;j++){
				T=new THREE.Vector4(t[j]*t[j]*t[j],t[j]*t[j],t[j],1);
				//T.applyMatrix4(MG);
				e=MG.elements;
				x=T.x*e[0]+T.y*e[1]+T.z*e[2]+T.w*e[3];
				y=T.x*e[4]+T.y*e[5]+T.z*e[6]+T.w*e[7];
				if(x<mostRight){
					return false;
				}else{
					mostRight=x;
				}
			}
		}
		return true;

	}
};
Curve.prototype.getBorder=function(type){
	if(!type){
		var type="CatMull-Rom";
	}
	var border={}
	border.top=-9e100;
	border.bottom=9e100;
	border.left=9e100;
	border.right=-9e100;
	if(type=="CatMull-Rom"){
		var M=new THREE.Matrix4(-0.5,1.5,-1.5,0.5,1,-2.5,2,-0.5,-0.5,0,0.5,0,0,1,0,0);
		var pList=[];
		var Mm,G,T,e,x,y,i,j,step,C0,C1,D0,D1;
		if(this.points.length<2){
			return true;
		}
		for(i=0;i<this.points.length-1;i++){
			C0=this.points[i];
			C1=this.points[i+1];
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

			Mm=M.clone();
			//G=numpy.matrix([D0,C0,C1,D1])
			G=new THREE.Matrix4(
					D0.x,D0.y,0,0,
					C0.x,C0.y,0,0,
					C1.x,C1.y,0,0,
					D1.x,D1.y,0,0);
			MG=Mm.multiply(G);
			t=[];
			step=0.1;
			for(j=0;j<1;j+=step){
				t.push(j);
			}
			t.push(1);
			for(j=0;j<t.length;j++){
				T=new THREE.Vector4(t[j]*t[j]*t[j],t[j]*t[j],t[j],1);
				//T.applyMatrix4(MG);
				e=MG.elements;
				x=T.x*e[0]+T.y*e[1]+T.z*e[2]+T.w*e[3];
				y=T.x*e[4]+T.y*e[5]+T.z*e[6]+T.w*e[7];

				if(x<border.left){
					border.left=x;
				}
				if(x>border.right){
					border.right=x;
				}
				if(y>border.top){
					border.top=y;
				}
				if(y<border.bottom){
					border.bottom=y;
				}
			}
		}
		return border;

	}
};
Curve.prototype.getPointX=function(targetX,type){
	if(!type){
		var type="CatMull-Rom";
	}
	var pos=new THREE.Vector2(0,0);
	if(type=="CatMull-Rom"){
		var M=new THREE.Matrix4(-0.5,1.5,-1.5,0.5,1,-2.5,2,-0.5,-0.5,0,0.5,0,0,1,0,0);
		var pList=[];
		var Mm,G,T,e,x,y,i,j,step,C0,C1,D0,D1;
		if(this.points.length<2){
			return pos;
		}
		for(i=0;i<this.points.length-1;i++){
			C0=this.points[i];
			C1=this.points[i+1];
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

			Mm=M.clone();
			//G=numpy.matrix([D0,C0,C1,D1])
			G=new THREE.Matrix4(
					D0.x,D0.y,0,0,
					C0.x,C0.y,0,0,
					C1.x,C1.y,0,0,
					D1.x,D1.y,0,0);
			MG=Mm.multiply(G);
			t=[];
			step=0.01;
			for(j=0;j<1;j+=step){
				t.push(j);
			}
			t.push(1);
			for(j=0;j<t.length;j++){
				T=new THREE.Vector4(t[j]*t[j]*t[j],t[j]*t[j],t[j],1);
				//T.applyMatrix4(MG);
				e=MG.elements;
				x=T.x*e[0]+T.y*e[1]+T.z*e[2]+T.w*e[3];
				y=T.x*e[4]+T.y*e[5]+T.z*e[6]+T.w*e[7];
		
				if(x-0.01<=targetX && x+0.01>=targetX){
					pos.x=x;
					pos.y=y;
					return pos;
				}
			}
		}
		return pos;
	}
};
