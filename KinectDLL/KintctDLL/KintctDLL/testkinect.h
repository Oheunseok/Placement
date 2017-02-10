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

#define BGCOUNT 50

#define CONTOURSIZE 50
#define CONTOURLEN 50
#define CONTOURRECT 500

template<class Interface>
inline void SafeRelease(Interface *& pInterfaceToRelease)
{
	if (pInterfaceToRelease != NULL)
	{
		pInterfaceToRelease->Release();
		pInterfaceToRelease = NULL;
	}
}



namespace TestKinect
{
	class TESTKINECT_API mKinect
	{
	private:
		
		///////////////////////////////// kinect var start
		IKinectSensor*	m_pKinectSensor;
		ICoordinateMapper*m_pCoordinateMapper;
		DepthSpacePoint* m_pDepthCoordinates;

		IMultiSourceFrameReader*m_pMultiSourceFrameReader;

		static const int        cDepthWidth = 512;
		static const int        cDepthHeight = 424;
		static const int        cColorWidth = 1920;
		static const int        cColorHeight = 1080;
		///////////////////////////////// kinect var end
		int m_a;
		float m_b;
		cv::Mat shadowImage;

		cv::Mat AddMat[BGCOUNT];

		//std::vector< std::vector< cv::Point> > contours;

		std::vector< std::vector< cv::Point> > true_touchcontours;  //Only mockup
		std::vector< std::vector< cv::Point> > false_touchcontours; //Only mockup


		cv::Mat mColorMat;
		cv::Mat mDepthMat;
		cv::Mat mDepthBufferMat;
		cv::Mat mCoordinateMat;
		cv::Mat mColorCopyMat;
		cv::Mat mWhiteMat;

		cv::Mat bgMat;

		cv::Mat diffMat;

		RGBQUAD* m_pColorFrameRGBX;
		RGBQUAD* m_pWhiteFrameRGBX;

		RGBQUAD*                m_pOutputRGBX;
		RGBQUAD*                m_pBackgroundRGBX;
		RGBQUAD*                m_pColorRGBX;
		UINT16 *depthBuffer = nullptr;

		INT64                   m_nStartTime;
		INT64                   m_nLastCounter;
		double                  m_fFreq;
		INT64                   m_nNextStatusTime;
		DWORD                   m_nFramesSinceUpdate;
		bool                    m_bSaveScreenshot;


		POINT* contours_list;
		int*contours_len = nullptr;
		int contours_size;
		int shadowImage_width, shadowImage_height;

		

	public:
		std::vector< std::vector< cv::Point> > contours;

		mKinect();
		~mKinect();

		void initialize();
		void Finalize();

		void set(int, float);
		void print();
		void get(int&, float&);

		int mockupLoadimage(const char*);

		int getShadowImageWidth(){ return shadowImage_width; }   // width 
		int getShadowImageHeight(){ return shadowImage_height; } // height

		///////////////// Touch
		POINT**getTouchList(bool);		//Only mockup. ��ġ ������� true ��ġ�� �ȵ� ������� false
		int*getTouchContourLen(bool);	//Only mockup. ������ ��ġ��������� ����.
		int getTouchContoursSize(bool);		//Only mockup. �������� ����.
		int touchmockupLoadimage(const char*, bool); //Only mockup. ��ġ �̹��� ���.
		void updateTouchContour();


		///////////////// contours �Ѱ��ִ� ����Ʈ.

		///////////////// contours�� ���͸� �Ѱ��ִ� ����Ʈ.
		int*getContourLen(); // ������ ���� ����. ��������� �ε��� ������ ����.
		POINT** getContours();
		POINT* getContourCenter();
		int getContoursSize(){ return contours_size; } // �������� ����.
		void updateContour();

		long getLen();

		///////////////// �׸��� �̹����� ����.
		unsigned char* getShadowImage();

		int createShadowImage();

		POINT** getImageContours(int num);
		POINT* getImageContoursCenter(int num);
		POINT** getTouchContours();
		HRESULT InitKinect();

		bool getCurrentFrame();

		void                    ProcessFrame(INT64 nTime,
			const UINT16* pDepthBuffer, int nDepthHeight, int nDepthWidth,
			const RGBQUAD* pColorBuffer, int nColorWidth, int nColorHeight,
			const BYTE* pBodyIndexBuffer, int nBodyIndexWidth, int nBodyIndexHeight);

		long imagecount;
		void processIncomingData();

		void getDepthImage(); /// depth mat �����.
		void createContours(int threshold);/// dpeth mat�� contour list �����.
		long getContoursCenterLen();		// contours center�� ���̸� �������ش�.
		void getContoursCenter();			// contours center�� �Ѱ��ش�.
		POINT mContoursCenter[500];

		POINT mContours[CONTOURSIZE][CONTOURLEN];

		POINT mContourRect[CONTOURRECT];

		long rectCount;

		void AddBackGround();
		void CreateBG();
		void DiffMat();
		void createContoursDiffMat();
		
		long CheckBG(const char*filename);

		void contoursRect(POINT*center,POINT*r);

		void KinectgetContours(POINT*list, long len);
		long getContoursLen();

		long contoursCount = 0;

		void closeWindow(){
			cv::destroyAllWindows();
		}


		/*bool CreateShadowImage(int MaxImageCount);
		POINT** getImageContours(int num);
		POINT* getImageContoursCenter(int num);
		POINT** getTouchContours();
		int InitKinect();*/
	};
}

