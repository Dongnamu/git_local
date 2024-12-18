# 이 파일에 filesData, treeData 등의 정적 데이터를 관리
filesData = {
    "button.js": {
        "code": """// button.js
export function Button(props) {
  console.log("Create a Button");
}""",
        "report": "button.js는 'components' 폴더 내 버튼 컴포넌트 예시입니다."
    },
    "modal.js": {
        "code": """// modal.js
export function Modal(props) {
  console.log("Create a Modal");
}""",
        "report": "modal.js는 'components' 폴더 내 모달 컴포넌트 예시입니다."
    },
    "main.js": {
        "code": """function add(a, b) {
  return a + b;
}
const result = add(2, 3);
console.log('main.js Result:', result);""",
        "report": "main.js: 프로젝트의 main 스크립트."
    },
    "utils.js": {
        "code": """export function multiply(a, b) {
  return a * b;
}
console.log("utils.js loaded");""",
        "report": "utils.js: 재사용 가능한 유틸 함수 모음."
    },
    "test.spec.js": {
        "code": """import { multiply } from '../src/utils.js';
test('multiply', () => {
  if (multiply(2, 3) !== 6) {
    throw new Error("Multiply test failed");
  }
});""",
        "report": "test.spec.js: multiply 함수를 테스트하는 간단한 유닛 테스트."
    },
    "readme.md": {
        "code": """# README
This is a sample README at the root level.
""",
        "report": "프로젝트 개요, 사용 방법 등을 설명하는 파일입니다."
    },
    "license.txt": {
        "code": """MIT License
Copyright ...
""",
        "report": "프로젝트의 라이센스 정보가 담긴 파일입니다."
    }
}

treeData = {
    "folders": {
        "src": {
            "folders": {
                "components": {
                    "folders": {},
                    "files": ["button.js", "modal.js"]
                }
            },
            "files": ["main.js", "utils.js"]
        },
        "test": {
            "folders": {},
            "files": ["test.spec.js"]
        }
    },
    "files": ["readme.md", "license.txt"]
}
