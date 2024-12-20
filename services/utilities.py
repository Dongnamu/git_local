import base64
import json
import time
import requests
import openai
from openai import APIError
openai.api_key = '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'
openai.organization = 'org-M2oxD2tCOmoMHTB7es7MLhSf'

def decode_files(blob):
    return base64.b64decode(blob).decode("utf-8")

def request_to_model(model, prompt):
    report_message = '''
당신은 코드를 리뷰하는 리뷰어 역할입니다. 당신은 코드 자체의 난이도와 완성도, 품질이 어떤지 리뷰하며, 주어진 코드의 보안적 결함성이 있는지 평가해야 합니다. 주어진 코드에 대해 평가문을 작성해 주시기를 바라며, 한국말로 작성주시기 바랍니다. 코드 수정 추천 문구는 작성하지 말아주시기 바랍니다.
다음은 예시 평가문입니다. 이를 참고하여 리뷰를 작성해 주세요. Markdown 문법을 사용하여 작성해주시기 바랍니다.

### 코드 리뷰 및 평가

---

#### **1. 코드의 난이도와 완성도**

- **난이도**:
  - Spring Boot를 사용한 REST 컨트롤러 구현은 초급에서 중급 수준의 개발자가 이해하고 작성할 수 있는 난이도로 보입니다.
  - 파일 업로드, 다운로드, 파일 목록 조회라는 일반적인 기능을 구현하고 있어, 난이도는 비교적 낮은 편입니다.

- **완성도**:
  - 코드의 주요 기능은 기본적으로 작동할 것으로 보입니다.
  - 하지만 코드 구조와 보안적 관점에서의 처리 부족으로 인해 완성도가 떨어지며 개선이 필요합니다.

---

#### **2. 코드 품질**

- **좋은 점**:
  1. Spring Boot의 REST 컨트롤러 구조를 적절히 활용하고 있습니다.
  2. 외부 설정 파일(`pvc.path`)을 `@Value` 어노테이션으로 주입받아 관리하는 점은 환경 설정 관리 측면에서 적합합니다.
  3. UTF-8 인코딩을 사용해 다운로드 파일명을 처리한 부분은 세부적인 배려를 보여줍니다.

- **개선이 필요한 점**:
  1. **파일 경로 관리**:
     - 파일 경로를 처리하는 부분에서 불필요하게 중복된 `File.separator`가 포함되어 있습니다.
     - Java의 `Paths.get` 또는 `Path.resolve`를 사용하면 경로를 더 안전하고 가독성 있게 관리할 수 있습니다.

  2. **예외 처리**:
     - `getFileItemList`, `upload`, `downloadAttach` 메서드에서 발생할 수 있는 예외를 포괄적으로 처리하고 있으나, 구체적인 에러 메시지가 부족합니다.
     - 예외를 분류하고 적절한 로그 메시지를 남기도록 개선해야 합니다.

  3. **리턴 데이터 구조**:
     - `getFileItemList` 메서드에서 파일 목록을 반환할 때 데이터 구조가 명확하지 않습니다.
     - API 응답으로 사용하는 데이터 구조를 명시적으로 선언하고 문서화하여 클라이언트가 이해하기 쉽게 해야 합니다.

  4. **로깅 부족**:
     - 메서드 내 로깅이 부족합니다. 특히 예외 발생 시 구체적인 정보를 로깅하여 문제를 추적할 수 있어야 합니다.

  5. **코드의 일관성**:
     - 일부 코드에서 경로를 처리하는 방식과 리턴 데이터 형식이 일관되지 않습니다.
     - 일관된 코딩 스타일과 API 설계 방식이 필요합니다.

---

#### **3. 보안적 결함 평가**

- **중요한 결함**:
  1. **디렉토리 트래버설 취약점**:
     - 파일명이나 경로를 검증하지 않아 디렉토리 트래버설 공격의 가능성이 존재합니다.
     - 예를 들어, `../`와 같은 상위 디렉토리 접근 시도를 차단해야 합니다.

  2. **파일 업로드 검증 부족**:
     - 업로드된 파일의 이름, 확장자, MIME 타입에 대한 검증이 없습니다.
     - 악의적인 파일 업로드를 방지하기 위해 허용된 파일 형식과 크기를 제한해야 합니다.

  3. **민감 정보 노출**:
     - `getFileItemList` 메서드에서 파일의 절대 경로를 클라이언트에 반환하고 있습니다.
     - 서버 내부 파일 시스템 구조를 외부에 노출하는 것은 보안적으로 매우 위험합니다.

  4. **경로 조작 가능성**:
     - `downloadAttach` 메서드에서 `fileName` 파라미터에 대한 검증이 없습니다.
     - 클라이언트가 악의적인 입력을 통해 임의의 파일을 다운로드할 가능성이 있습니다.

- **보완 방안**:
  1. **파일명 및 경로 검증**:
     - 업로드 및 다운로드 시 파일명을 검증하고, 허용되지 않은 문자를 필터링해야 합니다.
     - 파일 경로는 지정된 디렉토리 범위 내에서만 처리하도록 제한해야 합니다.
  2. **업로드 파일 제한**:
     - 업로드 가능한 파일 형식과 크기를 제한해야 합니다.
     - MIME 타입을 검증하고, 서버에서 처리되지 않는 파일은 삭제합니다.
  3. **민감 정보 보호**:
     - 절대 경로 대신 파일명이나 가공된 정보를 반환해야 합니다.
  4. **로그와 감사**:
     - 로깅을 통해 비정상적인 요청이나 예외를 기록하고, 보안 사고를 추적할 수 있도록 해야 합니다.

---

#### **4. 종합 의견**

이 코드는 기본적인 파일 관리 REST API 기능을 제공하지만, 보안적 결함과 구조적 개선 사항이 다수 존재합니다. 

- **가장 시급히 개선해야 할 사항**:
  1. 파일명 및 경로 검증 강화.
  2. 민감 정보 노출 방지.
  3. 업로드 및 다운로드 로직의 보안 강화.

- **추가 개선 사항**:
  1. 예외 처리 및 로깅 체계 보강.
  2. API 응답 데이터의 구조 명확화.
  3. 코드 스타일 및 경로 처리 방식의 일관성 확보.

이 코드는 현재 상태에서는 프로덕션 환경에 사용하기에는 위험 요소가 많습니다. 위의 보완점을 적용한 후 QA 테스트를 거쳐 배포를 고려할 것을 권장합니다. 
'''

    codeReview_message = '''
당신은 코드를 리뷰하며 코드 수정을 하는 역할을 담당하고 있습니다. import된 라이브러리나 class의 간략한 설명이 빠져있을 경우 해당 부분에 대한 주석을 달아야 합니다. import 한줄 한줄 세세하게 주석을 달아주시기 바랍니다. 구현 부분에서도 주석이 빠져있을 경우 주석을 달아주셔야 합니다. 또한, 각 function이 어떤 역할을 하는지 주석으로 달아주셔야 하며, 각 function마다 받는 parameter가 어떤 역할인지 java parameter 설명 형식을 따라서 주석 형태로 설명을 달아주셔야 합니다. 설명을 달 떄에는 한국말로 설명해주시기 바랍니다.
당신에게는 해당 코드에 대한 분석이 주어집니다. 분석을 토대로 코드를 수정하시기 바립니다. 당신이 코드를 삭제하거나 추가, 개선하는 부분이 있다면 해당 부분을 주석으로 표시해주시기 바랍니다. 만약 삭제를 했다면 comment out을 시킨 이후 주석으로 표시를 해주시기 바라며, 만약 추가하는 부분이 있다면 추가한 이후 주석으로 표시를 해주시기 바라며, 만약 개선하는 부분이 있다면, 개선 이전 코드를 comment out을 하고 주석으로 표시한 이후, 개선한 코드를 주석으로 표시해주시기 바랍니다.
개선된 코드를 작성하기 전에, 주석 / 삭제된 코드 / 수정된 코드 / 추가된 코드 세개의 섹션으로 분리해서 수정사항을 얘기해주시면서 어떻게 수정됐는지 코드도 설명 이후 같이 보여주시기 바라며, 그 이후 수정된 코드를 나타내주시기 바랍니다.  markdown 문법으로 작성해주세요.

다음은 작성 예시입니다. 이를 참고하여 작성해주세요.

### 수정사항 요약

#### 1. **주석 추가**
- `import`된 라이브러리에 설명 추가.
- 각 함수의 역할 설명과 파라미터에 대한 설명 추가.

#### 2. **코드 개선**
- `getFileItemList` 메서드에서 스트림을 사용한 코드를 개선하여 가독성을 높였습니다.
- 파일 저장 경로 설정에서 중복된 `File.separator` 제거.

---

### 주요 변경 사항 설명

#### **1. getFileItemList 메서드**
- 기존 코드:
  ```java
  List.of(files).stream().map(f -> Map.of(
      "name", f.getName(),
      "path", f.getAbsolutePath()));
  ```
- 개선 코드:
  ```java
  List<Map<String, String>> fileList = List.of(files).stream()
      .map(f -> Map.of(
          "name", f.getName(),
          "path", f.getAbsolutePath()))
      .toList();
  ```
  **변경 이유**: 가독성을 높이고 변수명을 추가해 코드 이해를 용이하게 함.

#### **2. 업로드 경로 설정**
- 기존 코드:
  ```java
  String saveName = pvcPath + File.separator + File.separator + file.getOriginalFilename();
  ```
- 개선 코드:
  ```java
  String saveName = pvcPath + File.separator + file.getOriginalFilename();
  ```
  **변경 이유**: `File.separator`가 중복 사용된 문제를 제거. 

#### **3. 주석 추가**
- 함수, 파라미터, `import`된 라이브러리에 상세한 설명 추가.

---

### 수정된 코드

```java
package com.example.demo.controller;

// File 관련 작업을 수행하기 위한 클래스
import java.io.File;
// 파일 입출력 예외 처리를 위한 클래스
import java.io.IOException;
// URL 관련 예외 처리를 위한 클래스
import java.net.MalformedURLException;
// 문자열을 특정 인코딩으로 변환하기 위한 클래스
import java.nio.charset.StandardCharsets;
// 파일 및 디렉토리 경로 조작을 위한 클래스
import java.nio.file.Path;
import java.nio.file.Paths;
// 여러 객체를 담는 리스트를 사용하기 위한 클래스
import java.util.List;
// Key-Value 쌍의 데이터를 저장하기 위한 클래스
import java.util.Map;

// Spring Framework의 설정 값을 주입받기 위한 어노테이션
import org.springframework.beans.factory.annotation.Value;
// 파일 리소스 관리를 위한 Spring Core 클래스
import org.springframework.core.io.Resource;
// URL 기반 리소스 관리를 위한 클래스
import org.springframework.core.io.UrlResource;
// HTTP 헤더 설정을 위한 클래스
import org.springframework.http.HttpHeaders;
// HTTP 상태 코드를 설정하기 위한 클래스
import org.springframework.http.HttpStatus;
// HTTP 응답을 구성하기 위한 클래스
import org.springframework.http.ResponseEntity;
// Spring Web 어노테이션으로 GET 요청을 처리하기 위한 클래스
import org.springframework.web.bind.annotation.GetMapping;
// URI 경로 변수 매핑을 위한 어노테이션
import org.springframework.web.bind.annotation.PathVariable;
// Spring Web 어노테이션으로 POST 요청을 처리하기 위한 클래스
import org.springframework.web.bind.annotation.PostMapping;
// URI 경로 매핑을 설정하기 위한 어노테이션
import org.springframework.web.bind.annotation.RequestMapping;
// HTTP 요청의 파라미터를 처리하기 위한 어노테이션
import org.springframework.web.bind.annotation.RequestParam;
// REST 컨트롤러를 정의하기 위한 어노테이션
import org.springframework.web.bind.annotation.RestController;
// 다중 파트 파일 업로드를 처리하기 위한 클래스
import org.springframework.web.multipart.MultipartFile;
// URI 관련 유틸리티 클래스
import org.springframework.web.util.UriUtils;

// 로깅 처리를 위한 Lombok 어노테이션
import lombok.extern.slf4j.Slf4j;

/**
 * 파일 관리 REST 컨트롤러
 */
@Slf4j
@RequestMapping("/api/files")
@RestController
public class FileRestController {
    
    // PVC 경로 설정 (설정 파일에서 값 주입)
    @Value("${pvc.path}")
    private String pvcPath;

    // 기본 생성자
    public FileRestController() {
    }
    
    /**
     * 파일 목록 조회 API
     *
     * @param id 파일 ID (선택)
     * @param keyword 검색 키워드 (선택)
     * @return 파일 목록 또는 에러 메시지
     */
    @GetMapping
    public ResponseEntity<?> getFileItemList(
            @PathVariable(name = "id", required = false) Long id, // 파일 ID
            @PathVariable(name = "keyword", required = false) String keyword // 검색 키워드
    ) {
        try {
            // PVC 디렉토리에서 파일 목록 가져오기
            File directory = new File(pvcPath);
            File[] files = directory.listFiles();

            if (files == null || files.length == 0) {
                return ResponseEntity.ok("No files found.");
            }

            // 파일 목록을 Map 형식으로 변환
            List<Map<String, String>> fileList = List.of(files).stream()
                    .map(f -> Map.of(
                            "name", f.getName(),
                            "path", f.getAbsolutePath()))
                    .toList();

            return ResponseEntity.ok(fileList);
        } catch (Exception e) {
            log.error("Error fetching file list", e);
            return new ResponseEntity<>(e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
    
    /**
     * 파일 업로드 API
     *
     * @param file 업로드할 파일
     * @return 성공 메시지 또는 에러 메시지
     */
    @PostMapping
    public ResponseEntity<?> upload(@RequestParam("file") MultipartFile file) {
        
        // 저장할 파일 이름 생성
        String saveName = pvcPath + File.separator + file.getOriginalFilename();
        Path savePath = Paths.get(saveName);

        try {
            // 파일 저장
            file.transferTo(savePath);
        } catch (IOException e) {
            log.error("File upload failed", e);
            return new ResponseEntity<>(e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
        }

        return ResponseEntity.ok().body("File uploaded successfully.");
    }
    
    /**
     * 파일 다운로드 API
     *
     * @param fileName 다운로드할 파일 이름
     * @return 파일 리소스 또는 에러 메시지
     * @throws MalformedURLException URL 형식 오류
     */
    @GetMapping("/download/{fileName}")
    public ResponseEntity<Resource> downloadAttach(@PathVariable("fileName") String fileName) throws MalformedURLException {
        // 다운로드할 파일 URL 리소스 생성
        UrlResource urlResource = new UrlResource("file:" + pvcPath + File.separatorChar + fileName);

        // 파일 이름 UTF-8로 인코딩
        String encodeUploadFileName = UriUtils.encode(fileName, StandardCharsets.UTF_8);
        // HTTP 헤더 설정 (파일 다운로드용)
        String contentDisposition = "attachment; filename=\"" + encodeUploadFileName + "\"";

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, contentDisposition)
                .body(urlResource);
    }
}
```
'''

    if model == 'qwen':
        return qwen_model(report_message, codeReview_message, prompt)
    elif model == 'gpt':
        return gpt_model(report_message, codeReview_message, prompt)
    else:
        raise NotImplementedError
    
def qwen_model(report_message, codeReview_message, prompt):
    URL = "http://125.7.137.190:8003/v2/models/coder-qwen-model/infer"
    
    messages = [
    {"role": "system", "content": report_message},
    {"role": "user", "content": prompt}
    ]
    
    # 요청 데이터 구성
    data = {
        "name": "summarization-model",
        "inputs": [
            {
                "name": "prompt",
                "shape": [len(messages)],
                "datatype": "BYTES",
                "data": [json.dumps(item) for item in messages]
            }
        ]
    }
    # JSON 데이터 직렬화 및 요청 전송
    json_str = json.dumps(data, ensure_ascii=False).encode('utf-8')
    report_res = requests.post(URL, data=json_str)
    
    report_result = report_res.json()['outputs'][0]['data'][0]
    
    messages = [
    {"role": "system", "content": codeReview_message},
    {"role": "user", "content": report_result + "\n\n" + prompt}
    ]
    
    # 요청 데이터 구성
    data = {
        "name": "summarization-model",
        "inputs": [
            {
                "name": "prompt",
                "shape": [len(messages)],
                "datatype": "BYTES",
                "data": [json.dumps(item) for item in messages]
            }
        ]
    }
    # JSON 데이터 직렬화 및 요청 전송
    json_str = json.dumps(data, ensure_ascii=False).encode('utf-8')
    codeReview_message = requests.post(URL, data=json_str)
    codeReview_message = codeReview_message.json()['outputs'][0]['data'][0]
    
    return report_result, codeReview_message


def gpt_model(report_message, codeReview_message, prompt):
    
    max_retries = 3
    retries = 0
    
    while retries < max_retries:
        try:    
            messages = [
            {"role": "system", "content": report_message},
            {"role": "user", "content": prompt}
            ]
            
            # 요청 데이터 구성
            chat = openai.ChatCompletion.create(
                        model="gpt-4o", messages=messages
                    )
            report_result = chat.choices[0].message.content
        except (APIError) as e:
            print("openai 서버가 과부하되었거나 아직 준비되지 않았습니다. 잠시 기다립니다...")
            time.sleep(60)  # 1분 기다린 후 다시 시도
            retries += 1
        
        retries = 0
        
        try:    
            messages = [
            {"role": "system", "content": codeReview_message},
            {"role": "user", "content": report_result + "\n\n" + prompt}
            ]
            
            # 요청 데이터 구성
            chat = openai.ChatCompletion.create(
                        model="gpt-4o", messages=messages
                    )
            codeReview_result = chat.choices[0].message.content
            break
        except (APIError) as e:
            print("openai 서버가 과부하되었거나 아직 준비되지 않았습니다. 잠시 기다립니다...")
            time.sleep(60)  # 1분 기다린 후 다시 시도
            retries += 1
            
    else:
        print('openai 서버가 응답하고 있지 않습니다. qwen 모델을 사용하여 리포트 작성을 시도합니다.')
        report_result, codeReview_result = qwen_model(report_message, codeReview_message, prompt)
        
    return report_result, codeReview_result