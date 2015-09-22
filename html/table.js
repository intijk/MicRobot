load("three.js")
var v=new THREE.Vector3();
var mapTable=[];
var variance=[];
var armSpringAngle, armFrontAngle,armAngle;
var cols=500;
var rows=250;
initMapTable();
print("init finish");
var total=0;
/*
for(armAngle=-90;armAngle<=90;armAngle++){
	for(armSpringAngle=-90;armSpringAngle<=90;armSpringAngle++){
		for(armFrontAngle=-90;armFrontAngle<=90;armFrontAngle++){
			var tipPos=getTipPos();
			var gridX=Math.round(tipPos.x*100/(cols/500))+cols/2;
			var gridY=Math.round(tipPos.y*100/(rows/250));
			ptVar=ptVariance(armAngle,armSpringAngle,armFrontAngle);
			if(ptVar<variance[gridX][gridY]){
				variance[gridX][gridY]=ptVar;
				mapTable[gridX][gridY]=[armAngle, armSpringAngle, armFrontAngle];	
				total+=1;
				//print("update");
				//print(gridX, gridY);
				//print(mapTable[gridX][gridY]);
				//print(tipPos);
			}
		}
	}
}
*/
//print(mapTable);
//print(total);
function ptVariance(a,b,c){
	var mean=(a+b+c)/3.0;
	return (a-mean)*(a-mean)+(b-mean)*(b-mean)+(c-mean)*(c-mean);
}
function initMapTable(){
	for(var i=0;i<=cols;i++){
		mapTable[i]=[];
		variance[i]=[];
		for(var j=0;j<=rows;j++){
			mapTable[i][j]=[-4,-4,-4];
			variance[i][j]=10000.0;
		}
	}
}
function getTipPos(){
	var tmpV=new THREE.Vector3(0,0,1);
	var axisH=new THREE.Vector3(0,0,1);
	var axisV=new THREE.Vector3(0,1,0);
	var dReferPoint=new THREE.Vector3(0,1,0);
	var curTip=new THREE.Vector3(0,0.51,0);


	var armLength=0.49;
	var armSpringLength=0.49;
	var armFrontLength=0.81;
	//axisH.applyAxisAngle(axisV,swingAngle);		
	dReferPoint.applyAxisAngle(axisH, armAngle/180*Math.PI);	
	tmpV.copy(dReferPoint);
	tmpV.multiplyScalar(armLength);
	curTip.add(tmpV);

	dReferPoint.applyAxisAngle(axisH, armSpringAngle/180*Math.PI);	
	tmpV.copy(dReferPoint);
	tmpV.multiplyScalar(armSpringLength);
	curTip.add(tmpV);
	
	dReferPoint.applyAxisAngle(axisH, armFrontAngle/180*Math.PI);	
	tmpV.copy(dReferPoint);
	tmpV.multiplyScalar(armFrontLength);
	curTip.add(tmpV);
	return curTip;
}
