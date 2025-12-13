class Loader:
    def __init__(self, connection):
        self.connection = connection

    def get_regex_configuration(self, product):
        """
        This method returns the product specific configuration

        :param product:
        :return: list of filtered/unfiltered events
        """
        with self.connection.cursor() as cur:
            query = f"""
                    SELECT regex_configuration
                    FROM product
                    where product_name='{product}'
                    """
            cur.execute(query)
            result = cur.fetchone()
            if result:
                return result[0]

        return None
