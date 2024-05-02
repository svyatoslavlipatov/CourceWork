//Import the THREE.js library
import * as THREE from "https://cdn.skypack.dev/three@0.129.0/build/three.module.js";
// To allow for the camera to move around the scene
import { OrbitControls } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/controls/OrbitControls.js";
// To allow for importing the .gltf file
import { GLTFLoader } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/loaders/GLTFLoader.js";

function init() {
  let container = document.getElementById("container3D");

  //Scene
  const scene = new THREE.Scene();

  //Camera
  const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.set(0.1, 0.1, 4);

  //render
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(1920, 1080);
  container.appendChild(renderer.domElement);

  const loader = new GLTFLoader();
  let obj = null;
  // Model
  {
    loader.load("./assets/model/KROL/scene.gltf", function (gltf) {
      obj = gltf;
      obj.scene.scale.set(0.3, 0.3, 0.3);
      scene.add(obj.scene);
    });
  }

  {
    const light = new THREE.DirectionalLight(0xffffff, 2);
    light.position.set(-10, 0, 10);
    light.lookAt(0, -2, 0);
    scene.add(light);

    const light2 = new THREE.DirectionalLight(0xffffff, 2);
    light.position.set(-10, 0, -10);
    light.lookAt(0, -2, 0);
    scene.add(light2);

    // Helper
    // const helper = new THREE.DirectionalLightHelper(light, 5);
    // scene.add(helper);
  }

  {
    const light = new THREE.DirectionalLight(0xffffff, 2);
    light.position.set(2, 0, 5);
    light.lookAt(0, 1, 0);
    scene.add(light);

    // Helper
    // const helper = new THREE.DirectionalLightHelper(light, 5);
    // scene.add(helper);
  }

  {
    const rectLight = new THREE.RectAreaLight(0x4123421, 1, 100, 100);
    rectLight.position.set(0, 0, 0);
    rectLight.rotation.y = Math.PI - Math.PI / 4;
    scene.add(rectLight);
  }

//   const controls = new OrbitControls(camera, renderer.domElement);
//   controls.autoRotate = false;
//   controls.autoRotateSpeed = 3;
//   controls.enableDamping = false;
//   controls.setMode("rotate");
//   controls.showX = false;
//   controls.showY = false;
//   controls.showZ = false;

  //Resize
  window.addEventListener("resize", onWindowResize, false);

  function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, window.innerHeight);
  }

  // Animate
  //   function animate() {
  //       requestAnimationFrame(animate)
  //       controls.update();
  //       renderer.render(scene, camera)
  //   }
  function animate() {
    requestAnimationFrame(animate);

    if (obj) obj.scene.rotation.y += 0.01;
    renderer.render(scene, camera);
  }
  animate();
}

init();
