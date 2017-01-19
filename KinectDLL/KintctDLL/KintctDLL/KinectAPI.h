#ifdef __cplusplus
#define EXTERNC extern "C"
#else
#define EXTERNC 
#endif

#ifdef KINTCTDLL_EXPORTS
#define TESTKINECT_API __declspec(dllexport)

#else
#define TESTKINECT_API __declspec(dllimport)
#endif

#include <Windows.h>

EXTERNC TESTKINECT_API long CreateImage();
EXTERNC TESTKINECT_API void InitKinect();
EXTERNC TESTKINECT_API void getContoursCenter(POINT*list, long len, long render);
EXTERNC TESTKINECT_API long ContoursLen();
EXTERNC TESTKINECT_API long ContoursCenterLen();
EXTERNC TESTKINECT_API void DepthImage(int threshold);

//EXTERNC TESTKINECT_API long Foopoint(POINT* batch, long bufferSize)
//{
//	for (size_t i = 0; i < bufferSize; i++)
//	{
//		batch[i].x = i;
//		batch[i].y = i;
//	}
//	return 0;
//}
//
//EXTERNC TESTKINECT_API long Foo(long* batch, long bufferSize)
//{
//	for (size_t i = 0; i < bufferSize; i++)
//	{
//		batch[i] = i;
//	}
//	return 0;
//}
//
//EXTERNC TESTKINECT_API void aa(){
//	printf("hello");
//}
//
//EXTERNC TESTKINECT_API POINT* getpointlist(){
//	POINT list[3];
//	for (int i = 0; i < 3; ++i){
//		list[i].x = i;
//		list[i].y = i;
//	}
//	return list;
//}
//
//EXTERNC TESTKINECT_API POINT getpoint(){
//	POINT list;
//	list.x = 3;
//	list.y = 4;
//	
//	return list;
//}
//
//EXTERNC TESTKINECT_API LONG* getlonglist(){
//	LONG list[3];
//	for (int i = 0; i < 3; ++i){
//		list[i] = i;
//	}
//	return list;
//}
//
//EXTERNC TESTKINECT_API LONG getlong(){
//	LONG list = 5;
//	
//	return list;
//}
//
//EXTERNC TESTKINECT_API int* getintarray(){
//	int list[3];
//	for (int i = 0; i < 3; ++i){
//		list[i] = i;
//	}
//	return list;
//}
//
//EXTERNC TESTKINECT_API int getint(){
//	int a = 4;
//	return a;
//}

class TESTKINECT_API KinectAPI{
private:

public:
	void print();
	void createimage(const char*);
	POINT** getContours();
	unsigned char* getShadowImage();
	void updateContour();
	int getContoursSize();
	POINT* getContourCenter(); 
	int*getContourLen();
	bool CreateShadowImage(int MaxImageCount);	// MaxImageCount에 만들어진 이미지의 개수를 넣어준다. 이미지는 만들어 놓은다.
	POINT** getImageContours(int num);			// Num에 따른 이미지의 contour list를 넘겨준다.
	POINT* getImageContoursCenter(int num);		// Num에 따른 이미지의 contour의 center list를 넘겨준다.
	POINT** getTouchContours();					// 키넥트 카메라의 최신 뎁스데이터를 가져온다. 뎁스데이터에 따른 contour list를 넘겨준다.
	int InitKinect();							// 키넥트 초기화에 따른 반환값을 넘겨준다. 현재는 0은 실패 1은 성공으로 본다.(단계 구분은 생략해본다)
	void saveImage();
	void processIncomingData();
};