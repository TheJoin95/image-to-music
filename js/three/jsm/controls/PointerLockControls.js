/**
* @author mrdoob / http://mrdoob.com/
*/

THREE.PointerLockControls = function ( camera ) {

	var scope = this;
	this.enabled = false;

	//reset camera
	camera.rotation.set( 0, 0, 0 );

	//From negative to positive
	//x-axis is left to right, y axis is bottom to top, z axis is back to front
	
	// pitch is rotations around x axis 
	var pitchObject = new THREE.Object3D();
	pitchObject.add( camera );

	//rotations around the vertical y axis
	var yawObject = new THREE.Object3D();
	yawObject.position.y = 1.75;
	yawObject.add( pitchObject );
		
	//Hierarchy: yawObject -> pitchObject -> camera

	var PI_2 = Math.PI / 2;

	var onMouseMove = function ( event ) {

		//if camera not allowed to move, exit.
		if ( scope.enabled === false ) return;

		//since we locked the pointer, movementX and movementY is the number of pixels the mouse
		//has moved since the last onMouseMove function was executed.
		//screenX, screenY which return horizontal and vertical distance are now constants
		var movementX = event.movementX || event.mozMovementX || event.webkitMovementX || 0;
		var movementY = event.movementY || event.mozMovementY || event.webkitMovementY || 0;

		//for the current animation frame, rotate our camera object by the change in pixels 
		//multiplied by a constant. 
		yawObject.rotation.y -= movementX * 0.002;
		pitchObject.rotation.x -= movementY * 0.002;
        
        //only the box collider surrounding the user should not rotate around any axis
        camera.children[0].rotation.y += movementX * 0.002;
        camera.children[0].rotation.x += movementY * 0.002;

		//we want to constrain how far the user can rotate around the x-axis.
		//Our bounds are [-PI/2, PI/2] so we can only rotate 90 degrees up or down from
		//the horizon. As such, the following line states that as long as the given rotation, 
		//around the x axis, from the mouse is in between our bounds, assign that value, else,
		//assign the upper or lower bound that it exceeds instead.
		pitchObject.rotation.x = Math.max( - PI_2, Math.min( PI_2, pitchObject.rotation.x ) );
        camera.children[0].rotation.x = Math.max( - PI_2, Math.min( PI_2, camera.children[0].rotation.x ) );

	};

	//remove the controls on this camera
	this.dispose = function() {

		document.removeEventListener( 'mousemove', onMouseMove, false );

	}

	//continuously check for mousemovent, if there is movement, execute
	//the function onMouseMove, detailed above
	document.addEventListener( 'mousemove', onMouseMove, false );


	//returns parent object that contains the two rotations and camera
	this.getObject = function () {
		return yawObject;
	};

	this.getDirection = function() {

		// assumes the camera itself is not rotated
		/*
		var direction = new THREE.Vector3( 0, 0, - 1 );
		var rotation = new THREE.Euler( 0, 0, 0, "YXZ" );
		//defines rotation around axis in given order

		return function( v ) { //v is a THREE.Vector3 object

			//why???	
			rotation.set( pitchObject.rotation.x, yawObject.rotation.y, 0 );

			//http://threejs.org/docs/#Reference/Math/Vector3.copy
			//http://threejs.org/docs/#Reference/Math/Vector3.applyEuler
			v.copy( direction ).applyEuler( rotation );

			return v;

		}
		*/
	}();

};
